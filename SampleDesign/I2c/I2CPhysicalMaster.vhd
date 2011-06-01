--=============================================================================--
--   Title & version       : I2cPhysicalMaster
--   Company               : EnjoyDigital
--   Filename              : I2cPhysicalMaster.vhd
--   Date (yyyy-mm-dd)     : 07/05/2011
--   Purpose               : I2C Physical Master
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
use work.GlobalTypes.all;
use work.I2cPack.all;

--============================================================================--
--                             Entity
--============================================================================--
--* @link     [entity] [I2cPhysicalMaster]
--* @brief    I2c Physical Master Atomics Operations
-------------------------------------------------------------------------------
entity I2CPhysicalMaster is
  generic(
    FCLK  : real := 50.0;               --Clock Frequency (Mhz)
    SPEED : real := 100.0               --I2c Speed (Kbit/s)
    );
  port (
    -- Clock/Reset
    Clk  : in std_logic;
    RstN : in std_logic;

    -- Physical Layer
    PhysSclOut   : out   std_logic;
    PhysSdaInOut : inout std_logic;

    -- Logical Layer
    -- Control
    LogEnable    : in  std_logic;       -- Start an operation
    LogOperation : in  I2C_PHYSICAL_AT_OP;  -- Operation required
    LogDone      : out std_logic;       -- Indicates Master is done (not busy)

    --Data
    LogDataIn   : in  std_logic_vector(7 downto 0);  -- Data from Master to I2C Bus
    LogDataOut  : out std_logic_vector(7 downto 0);  -- Data from I2C Bus (slave) to Master
    LogSlaveAck : out std_logic);  -- Acknowledge level from slave (on write)
end I2cPhysicalMaster;


--============================================================================--
--                               Architecture
--============================================================================--
architecture Rtl of I2cPhysicalMaster is

  --===================================--
  -- Types Declaration
  --===================================--
  type STATES is (A, B, C, D, IDLE);

  --===================================--
  -- Components Declaration
  --===================================--
  -- NA
  --===================================--
  -- Constants Declaration
  --===================================--
  -- TICK_NUM controls the I2C bus timing. 
  -- TICKNUM = (FCLK*10^6 / (4 * SPEED*10^3)) - 2
  -- Example:
  --   FCLK:  50 MHz Clock
  --   SPEED: 100 kbit/s (Standard mode)
  --   TICK_NUM = (50000000 / (4 * 100000)) - 2
  --            = 123 
  constant TICK_NUM : integer := integer(FCLK*1.0E6/(4.0*SPEED*1.0E3))-2;

  --===================================--
  -- Signals Declaration
  --===================================--
  --Control
  signal bitCount : integer range 0 to 8;
  signal timer    : integer range 0 to TICK_NUM;
  signal busy     : std_logic;

  --State
  signal state       : STATES;
  signal delayEnable : std_logic;

  --Command
  signal op      : I2C_PHYSICAL_AT_OP;
  signal dataIn  : std_logic_vector(8 downto 0);
  signal dataOut : std_logic_vector(7 downto 0);
  signal ack     : std_logic;

  --TriState Sda
  signal physSdaOut : std_logic;
  signal physSdaIn  : std_logic;

  signal logDone_i   : std_logic;
  signal logDone_i_d : std_logic;

begin

  ---------------------------------------------------------  
  -- PhysicalController Process                          --
  ---------------------------------------------------------
  PhysicalController_P : process(Clk, RstN)
  begin
    -- Reset
    if (RstN = '0') then
      
      bitCount <= 0;
      timer    <= 0;
      busy     <= '0';

      state       <= A;
      delayEnable <= '0';

      op      <= I2C_START;
      dataIn  <= (others => '0');
      dataOut <= (others => '0');
      ack     <= '0';

      LogDataOut  <= (others => '0');
      LogSlaveAck <= '0';
      logDone_i   <= '0';
      logDone_i_d <= '0';

      PhysSclOut <= '1';                -- SCL pulled high
      physSdaOut <= '1';                -- SDA pulled high

      -- Rising Edge of Clk
    elsif (rising_edge(Clk)) then

      -- If Not Busy Wait for Command
      if (busy = '0') then
        
        if (LogEnable = '1') then
          busy      <= '1';
          state     <= A;
          op        <= LogOperation;
          dataOut   <= LogDataIn;
          bitCount  <= 0;
          logDone_i <= '0';
        end if;

        -- Wait If In Delay Loop
      elsif (delayEnable = '1') then
        
        if (timer = TICK_NUM) then
          timer       <= 0;
          delayEnable <= '0';
        else
          timer <= timer + 1;
        end if;

        -- Else Execute Command
      else
        
        case state is
          
          when A =>
            state       <= B;
            delayEnable <= '1';

            case op is
              when I2C_START =>
                PhysSclOut <= '1';      -- SCL pulled high
                physSdaOut <= '1';      -- SDA pulled high

              when I2C_RESTART =>
                PhysSclOut <= '0';      -- SCL driven low
                physSdaOut <= '1';      -- SDA pulled high

              when I2C_STOP =>
                PhysSclOut <= '0';      -- SCL driven low
                physSdaOut <= '0';      -- SDA driven low

              when I2C_WRITE_DATA =>
                PhysSclOut <= '0';      -- SCL driven low

                if (bitCount = 8) then
                  PhysSdaOut <= '1';    -- SDA pulled high (Allow slave ack)
                else
                  PhysSdaOut <= dataOut(7);  -- SDA set by data bit
                end if;

              when I2C_READ_DATA_ACK =>
                PhysSclOut <= '0';      -- SCL driven low
                if (bitCount = 8) then
                  physSdaOut <= '0';    -- SDA driven low (Set Ack bit)
                else
                  physSdaOut <= '1';    -- SDA pulled high (Allow slave write)
                end if;

              when I2C_READ_DATA_NACK =>
                PhysSclOut <= '0';      -- SCL driven low
                physSdaOut <= '1';  -- SDA pulled high (Set Nack bit or allow slave write)

            end case;

            dataOut <= dataOut(6 downto 0) & '0';

          when B =>
            state       <= C;
            delayEnable <= '1';

            case op is
              when I2C_START =>
                PhysSclOut <= '1';      -- SCL pulled high
                physSdaOut <= '1';      -- SDA pulled high

              when I2C_RESTART =>
                PhysSclOut <= '1';      -- SCL pulled high
                physSdaOut <= '1';      -- SDA pulled high

              when I2C_STOP =>
                PhysSclOut <= '1';      -- SCL pulled high
                physSdaOut <= '0';      -- SDA driven low

              when I2C_WRITE_DATA =>
                PhysSclOut <= '1';      -- SCL pulled high

              when I2C_READ_DATA_ACK =>
                PhysSclOut <= '1';      -- SCL pulled high

              when I2C_READ_DATA_NACK =>
                PhysSclOut <= '1';      -- SCL pulled high

            end case;

          when C =>
            state       <= D;
            delayEnable <= '1';

            case op is
              when I2C_START =>
                PhysSclOut <= '1';      -- SCL pulled high
                physSdaOut <= '0';      -- SDA driven low

              when I2C_RESTART =>
                PhysSclOut <= '1';      -- SCL pulled high
                physSdaOut <= '0';      -- SDA driven low

              when I2C_STOP =>
                PhysSclOut <= '1';      -- SCL pulled high
                physSdaOut <= '1';      -- SDA pulled high

              when I2C_WRITE_DATA =>
                PhysSclOut <= '1';      -- SCL pulled high

                if (bitCount = 8) then
                  ack <= physSdaInOut;  -- Read Slave Acknowledge
                end if;

              when I2C_READ_DATA_ACK =>
                PhysSclOut <= '1';      -- SCL pulled high
                dataIn     <= dataIn(7 downto 0) & PhysSdaInOut;

              when I2C_READ_DATA_NACK =>
                PhysSclOut <= '1';      -- SCL pulled high
                dataIn     <= dataIn(7 downto 0) & PhysSdaInOut;

            end case;

          when D =>
            delayEnable <= '1';

            case op is
              when I2C_START =>
                PhysSclOut <= '0';      -- SCL driven low
                physSdaOut <= '0';      -- SDA driven low

              when I2C_RESTART =>
                PhysSclOut <= '0';      -- SCL driven low
                physSdaOut <= '0';      -- SDA driven low

              when I2C_STOP =>
                PhysSclOut <= '1';      -- SCL pulled high
                physSdaOut <= '1';      -- SDA pulled high

              when I2C_WRITE_DATA =>
                PhysSclOut <= '0';      -- SCL driven low
              when I2C_READ_DATA_ACK =>
                PhysSclOut <= '0';      -- SCL driven low
              when I2C_READ_DATA_NACK =>
                PhysSclOut <= '0';      -- SCL driven low

            end case;

            case op is

              --One Bit Operation
              when I2C_START | I2C_RESTART | I2C_STOP =>
                state <= IDLE;

                --Eight Bit Operation
              when I2C_WRITE_DATA | I2C_READ_DATA_ACK | I2C_READ_DATA_NACK =>
                if (bitCount = 8) then
                  state <= IDLE;
                else
                  bitCount <= bitCount + 1;
                  state    <= A;
                end if;
                
            end case;

          when IDLE =>
            busy      <= '0';
            logDone_i <= not DelayEnable;

            -- Ouptut Data on Read
            if (op = I2C_READ_DATA_ACK or op = I2C_READ_DATA_NACK) then
              LogDataOut <= dataIn(8 downto 1);
            end if;

            -- Output Ack on Write
            if (op = I2C_WRITE_DATA or op = I2C_READ_DATA_ACK) then
              LogSlaveAck <= ack;
            end if;

        end case;

      end if;


      logDone_i_d <= logDone_i;
      
    end if;

  end process PhysicalController_P;

  -- Tri-State On Sda
  PhysSdaInOut <= '0' when physSdaOut = '0' else
                  'Z';

  --Output LogDone
  LogDone <= logDone_i and (not logDone_i_d);

end Rtl;
