--=============================================================================--
--   Title & version       : Wm8731Driver
--   Company               : EnjoyDigital
--   Filename              : Wm8731Driver.vhd
--   Date (yyyy-mm-dd)     : 07/05/2011
--   Purpose               : Wm8731 Driver for AppleIISoC
--                           
--   Level of description  : RTL
--   Limitations           : 
--   Authors               : F. KERMARREC
--   Projects              : 
--   Tools & tools versions: 
--   Reference             : 
--   Coding Standards      : EnjoyDigital VHDL Coding Rules
--   Notes                 : 
--------------------------------------------------------------------------------
--   History               :
--------------------------------------------------------------------------------
--   Version               : 00.00
--   Date (yyyy-mm-dd)     : 07/05/2011
--   Authors               : F. KERMARREC
--   Purpose               : First Revision
--============================================================================--
--  
-- Copyright (c) 2011  Enjoy-Digital Florent Kermarrec <florent@enjoy-digital.fr>  
--  
--  This file is free software: you may copy, redistribute and/or modify it  
--  under the terms of the GNU General Public License as published by the  
--  Free Software Foundation, either version 2 of the License, or (at your  
--  option) any later version.  
--  
--  This file is distributed in the hope that it will be useful, but  
--  WITHOUT ANY WARRANTY; without even the implied warranty of  
--  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU  
--  General Public License for more details.  
--  
--  You should have received a copy of the GNU General Public License
--  along with this program.  If not, see <http://www.gnu.org/licenses/>.  
--============================================================================--

--============================================================================--
--                            Libraries
--============================================================================--
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.I2cPack.all;

--============================================================================--
--                             Entity
--============================================================================--
--* @link     [entity] [Wm8731Driver]
--* @brief    Wm8731Driver I2c initialization and I2S Audio Interface
-------------------------------------------------------------------------------
entity Wm8731Driver is
  port (
    -- Clock/Reset
    Clk  : in std_logic;
    RstN : in std_logic;

    --Audio
    AudioData : in unsigned(15 downto 0);

    --I2c Interface
    I2cScl : out   std_logic;           --I2c Clock
    I2cSda : inout std_logic;           --I2c Data

    --I2s Interface
    I2sAdcLrCk : inout std_logic;       -- ADC LR Clock
    I2sAdcDat  : in    std_logic;       -- ADC Data
    I2sDacLrCk : inout std_logic;       -- DAC LR Clock
    I2sDacDat  : out   std_logic;       -- DAC Data
    I2sBClk    : inout std_logic;       -- Bit-Stream Clock
    I2sXCk     : out   std_logic        -- Chip Clock
    );
end Wm8731Driver;


--============================================================================--
--                            Architecture
--============================================================================--
architecture Rtl of Wm8731Driver is

  --===================================--
  -- Constants Declaration
  --===================================--
  --Wm8731 Address
  constant WM8731_I2C_ADDR : unsigned(7 downto 0) := X"1A";

  --===================================--
  -- Components Declaration
  --===================================--
  component I2cMaster
    generic (
      FCLK  : real;
      SPEED : real);
    port (
      PeriphClk     : in    std_logic;
      PeriphRstN    : in    std_logic;
      PeriphCeN     : in    std_logic;
      PeriphAddr    : in    unsigned(3 downto 0);
      PeriphDataIn  : in    unsigned(7 downto 0);
      PeriphDataOut : out   unsigned(7 downto 0);
      PeriphWeN     : in    std_logic;
      PeriphAckN    : out   std_logic;
      PeriphIntAN   : out   std_logic;
      PhysSclOut    : out   std_logic;
      PhysSdaInOut  : inout std_logic);
  end component;


  --===================================--
  -- Signals Declaration
  --===================================--
  --I2C Interface
  signal i2cPeriphAddr    : unsigned(3 downto 0);
  signal i2cPeriphDataIn  : unsigned(7 downto 0);
  signal i2cPeriphDataOut : unsigned(7 downto 0);
  signal i2cPeriphWeN     : std_logic;
  signal i2cPeriphAckN    : std_logic;
  signal i2cPeriphIntAN   : std_logic;

  --I2C State Machine
  type wmConfigStateType is (IDLE,
                             GET_CMD,
                             WRITE_WM8731_ADDR,
                             WRITE_ADDR,
                             WRITE_DATA,
                             SEND_DATA,
                             CLEAR_START,
                             WAIT_ACK);
  signal wmConfigState : wmConfigStateType;
  signal wmConfigData  : unsigned(7 downto 0);
  signal wmConfigAddr  : unsigned(7 downto 0);
  signal cmdCpt        : unsigned(3 downto 0);

  --I2S Interface
  signal lrClk          : std_logic;
  signal bClk           : std_logic;
  signal xClk           : std_logic;
  signal lrClkCnt       : unsigned(7 downto 0);
  signal bClkCnt        : unsigned(3 downto 0);
  signal setBClk        : std_logic;
  signal setLrClk       : std_logic;
  signal clrBClk        : std_logic;
  signal shiftAudioData : unsigned(15 downto 0);
  
begin
  ---------------------------------------------------------  
  -- Static Affectations                                 --
  ---------------------------------------------------------

  ---------------------------------------------------------  
  -- Wm8731 I2c Configuration                            --
  ---------------------------------------------------------
  Wm8731Configuration_P : process(Clk, RstN)
  begin
    if RstN = '0' then
      
      wmConfigState   <= GET_CMD;
      cmdCpt          <= (others => '0');
      wmConfigData    <= (others => '0');
      wmConfigAddr    <= (others => '0');
      i2cPeriphAddr   <= (others => '0');
      i2cPeriphDataIn <= (others => '0');
      i2cPeriphWeN    <= '1';

    elsif rising_edge(Clk) then
      case wmConfigState is

        --Get Next I2c Command to Send
        when GET_CMD =>
          case cmdCpt is
            when X"0"   => wmConfigData <= X"1A"; wmConfigAddr <= X"00";  -- LIN_L
            when X"1"   => wmConfigData <= X"1A"; wmConfigAddr <= X"01";  -- LIN_R
            when X"2"   => wmConfigData <= X"7B"; wmConfigAddr <= X"02";  -- HEAD_L
            when X"3"   => wmConfigData <= X"7B"; wmConfigAddr <= X"03";  -- HEAD_R
            when X"4"   => wmConfigData <= X"F8"; wmConfigAddr <= X"04";  -- A_PATH_CTRL
            when X"5"   => wmConfigData <= X"06"; wmConfigAddr <= X"05";  -- D_PATH_CTRL
            when X"6"   => wmConfigData <= X"00"; wmConfigAddr <= X"06";  -- POWER_ON
            when X"7"   => wmConfigData <= X"01"; wmConfigAddr <= X"07";  -- SET_FORMAT
            when X"8"   => wmConfigData <= X"02"; wmConfigAddr <= X"08";  -- SAMPLE_CTRL
            when X"9"   => wmConfigData <= X"01"; wmConfigAddr <= X"09";  -- SET_ACTIVE
            when others => null;
          end case;

          cmdCpt <= cmdCpt+1;

          if cmdCpt >= X"A" then
            wmConfigState <= IDLE;
          else
            wmConfigState <= WRITE_WM8731_ADDR;
          end if;
          
         --Write Slave Addr in Register
        when WRITE_WM8731_ADDR =>
          i2cPeriphAddr   <= to_unsigned(REG_ADDR, 4);
          i2cPeriphDataIn <= WM8731_I2C_ADDR;
          i2cPeriphWeN    <= '0';
          wmConfigState   <= WRITE_ADDR;

          --Write Slave Addr in Register
        when WRITE_ADDR =>
          i2cPeriphAddr   <= to_unsigned(REG_WRITE_DATA, 4);
          i2cPeriphDataIn <= wmConfigAddr;
          i2cPeriphWeN    <= '0';
          wmConfigState   <= WRITE_DATA;

          --Write Data in Write Register 0
        when WRITE_DATA =>
          i2cPeriphAddr   <= to_unsigned(REG_WRITE_DATA+1, 4);
          i2cPeriphDataIn <= wmConfigData;
          i2cPeriphWeN    <= '0';
          wmConfigState   <= SEND_DATA;

          --Send Data to slave over I2c
        when SEND_DATA =>
          i2cPeriphAddr   <= to_unsigned(REG_CONTROL, 4);
          i2cPeriphDataIn <= b"00000101";
          i2cPeriphWeN    <= '0';
          wmConfigState   <= CLEAR_START;

          --Send Data to slave over I2c
        when CLEAR_START =>
          i2cPeriphAddr   <= to_unsigned(REG_CONTROL, 4);
          i2cPeriphDataIn <= b"00000100";
          i2cPeriphWeN    <= '0';
          wmConfigState   <= WAIT_ACK;

          --Wait I2c to finish
        when WAIT_ACK =>
          i2cPeriphWeN <= '1';
          if i2cPeriphAckN = '0' then
            wmConfigState <= GET_CMD;
          end if;

          -- IDLE (Dead End)
        when others =>
          null;
      end case;
      
    end if;
  end process Wm8731Configuration_P;

  ---------------------------------------------------------  
  -- I2cMaster                                           --
  ---------------------------------------------------------
  I2cMaster_1 : I2cMaster
    generic map (
      FCLK  => 14.0,                    --14 MHz Clock
      SPEED => 100.0)                   --100 Kbits/s Speed
    port map (
      PeriphClk     => Clk,
      PeriphRstN    => RstN,
      PeriphCeN     => '0',
      PeriphAddr    => i2cPeriphAddr,
      PeriphDataIn  => i2cPeriphDataIn,
      PeriphDataOut => i2cPeriphDataOut,
      PeriphWeN     => i2cPeriphWeN,
      PeriphAckN    => i2cPeriphAckN,
      PeriphIntAN   => i2cPeriphIntAN,
      PhysSclOut    => I2cScl,
      PhysSdaInOut  => I2cSda);

  -- LrClk Divider 
  -- Audio chip main clock is 18.432MHz / Sample rate 48KHz
  -- Divider is 18.432 MHz / 48KHz = 192 (X"C0")
  -- Left justify mode set by I2c Controller
  LrClkCnt_P : process (Clk,RstN)
  begin
    if RstN = '0' then
      LrClkCnt <= (others => '0');
    elsif rising_edge(Clk) then
      if LrClkCnt = x"BF" then
        LrClkCnt <= (others => '0');
      else
        LrClkCnt <= LrClkCnt + 1;
      end if;
    end if;
  end process LrClkCnt_P;

  setLrClk <= '1' when LrClkCnt = X"BF" else '0';

  -- bClk Divider 
  bClkCnt_P : process (Clk,RstN)
  begin
    if RstN = '0' then
      bClkCnt <= (others => '0');
    elsif rising_edge(Clk) then
      if bClkCnt = X"B" or setLrClk = '1' then
        bClkCnt <= X"0";
      else
        bClkCnt <= bClkCnt + 1;
      end if;
    end if;
  end process bClkCnt_P;

  setBClk <= '1' when bClkCnt(3 downto 0) = "0101" else '0';
  clrBClk <= '1' when bClkCnt(3 downto 0) = "1011" else '0';

  -- lrClk Generation 
  lrClk_P : process (Clk,RstN)
  begin
    if RstN = '0' then
      lrClk <= '0';
    elsif rising_edge(Clk) then
      if setLrClk = '1' then
        lrClk <= not lrClk;
      end if;
    end if;
  end process lrClk_P;

  -- bClk Generation 
  bClk_P : process (Clk,RstN)
  begin
    if RstN = '0' then
      bClk <= '0';
    elsif rising_edge(Clk) then
      if setLrClk = '1' or clrBClk = '1' then
        bClk <= '0';
      elsif setBClk = '1' then
        bClk <= '1';
      end if;
    end if;
  end process bClk_P;

  -- Audio data shift output
  shiftAudio_P : process (Clk,RstN)
  begin
    if RstN = '0' then
      shiftAudioData <= (others => '0');
     elsif rising_edge(clk) then
        if setLrClk = '1' then
          shiftAudioData <= AudioData;
        elsif clrBClk = '1' then
          shiftAudioData <= shiftAudioData(14 downto 0) & '0';
        end if;
      end if;
  end process shiftAudio_P;

  -- Generate Audio Outputs
  I2sAdcLrCk <= lrClk;
  I2sDacLrCk <= lrClk;
  I2sDacDat  <= shiftAudioData(15);
  I2sBClk    <= bClk;
  I2sXCk     <= Clk;
  
end Rtl;
