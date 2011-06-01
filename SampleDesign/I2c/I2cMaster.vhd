--=============================================================================--
--   Title & version       : I2cMaster
--   Company               : EnjoyDigital
--   Filename              : I2cMaster.vhd
--   Date (yyyy-mm-dd)     : 07/05/2011
--   Purpose               : I2C Master
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
--* @link     [entity] [I2cMaster]
--* @brief    I2c Master Controller
-------------------------------------------------------------------------------
entity I2cMaster is
  generic(
    FCLK  : real := 50.0;               --Clock Frequency (Mhz)
    SPEED : real := 100.0               --I2c Speed (Kbit/s)
    );
  port (
    -- Periph Standard Interface
    PeriphClk     : in  std_logic;
    PeriphRstN    : in  std_logic;
    PeriphCeN     : in  std_logic;
    PeriphAddr    : in  unsigned(3 downto 0);
    PeriphDataIn  : in  unsigned(7 downto 0);
    PeriphDataOut : out unsigned(7 downto 0);
    PeriphWeN     : in  std_logic;
    PeriphAckN    : out std_logic;
    PeriphIntAN   : out std_logic;

    -- Physical Layer
    PhysSclOut   : out   std_logic;
    PhysSdaInOut : inout std_logic
    );
end I2cMaster;

architecture Rtl of I2cMaster is

  --===================================--
  -- Constants Declaration
  --===================================--
  --Register Mapping
  -- REG_CONTROL:
  --   [0]    : Start I2c Write
  --   [1]    : Start I2c Read
  --   [3..2] : Acces Size (0 to 3)
  --   [4]    : Clear Ack Error
  --   [7..4] : 
  -- REG_STATUS:
  --   [0]    : I2c Write Done
  --   [1]    : I2c Read Done
  --   [2]    : I2c Busy
  --   [4]    : Spare
  --   [5]    : Ack Error Detected
  --   [7..6] : Spare
  -- REG_ADDR:
  --   [7..0] : I2c Slave Address
  -- REG_WRITE_DATA:
  --   [0][7..0] : I2c Write Data 1
  --   [1][7..0] : I2c Write Data 2
  --   [2][7..0] : I2c Write Data 3
  --   [3][7..0] : I2c Write Data 4
  -- REG_READ_DATA:
  --   [0][7..0] : I2c Read Data 1
  --   [1][7..0] : I2c Read Data 2
  --   [2][7..0] : I2c Read Data 3
  --   [3][7..0] : I2c Read Data 4


  --===================================--
  -- Components Declaration
  --===================================--
  component I2CPhysicalMaster
    generic (
      FCLK  : real;
      SPEED : real);
    port (
      Clk          : in    std_logic;
      RstN         : in    std_logic;
      PhysSclOut   : out   std_logic;
      PhysSdaInOut : inout std_logic;
      LogEnable    : in    std_logic;
      LogOperation : in    I2C_PHYSICAL_AT_OP;
      LogDone      : out   std_logic;
      LogDataIn    : in    std_logic_vector(7 downto 0);
      LogDataOut   : out   std_logic_vector(7 downto 0);
      LogSlaveAck  : out   std_logic);
  end component;

  --===================================--
  -- Signals Declaration
  --===================================--
  --Registers
  type registersType is array (natural range 0 to REGISTER_NB-1) of unsigned(REGISTER_SIZE-1 downto 0);
  signal registersRW        : registersType;
  signal registersRONLY     : registersType;
  signal regControl_d       : unsigned(REGISTER_SIZE-1 downto 0);
  signal registersAccesMode : unsigned(REGISTER_NB-1 downto 0);

  --Registers <--> Physical Manager
  signal i2cStartWrite    : std_logic;
  signal i2cStartRead     : std_logic;
  signal i2cAccesSize     : unsigned(1 downto 0);
  signal i2cAckErrorClear : std_logic;

  -- Physical Manager States Signals
  type physicalStateType is (IDLE,
                             START,
                             STOP,
                             WRITE_ADDR,
                             WRITE_DATA,
                             READ_DATA,
                             WAIT_FOR_DONE);
  signal physicalState     : physicalStateType;
  signal nextPhysicalState : physicalStateType;
  signal i2cWriteOnGoing   : std_logic;
  signal i2cReadOnGoing    : std_logic;
  signal i2cAccesCpt       : unsigned(1 downto 0);
  signal i2cAccesDone      : std_logic;
  signal i2cAckError       : std_logic;

  -- Physical Master Wrapper Signals
  signal logEnable     : std_logic;
  signal logOperation  : I2C_PHYSICAL_AT_OP;
  signal logDone       : std_logic;
  signal logDataIn     : unsigned(REGISTER_SIZE-1 downto 0);
  signal logDataOut    : unsigned(REGISTER_SIZE-1 downto 0);
  signal logDataInStd  : std_logic_vector(REGISTER_SIZE-1 downto 0);
  signal logDataOutStd : std_logic_vector(REGISTER_SIZE-1 downto 0);
  signal logSlaveAck   : std_logic;

begin
  ---------------------------------------------------------  
  -- Static Affectations                                 --
  ---------------------------------------------------------
  --Registers Modes
  registersAccesMode(REG_CONTROL)        <= RW;
  registersAccesMode(REG_STATUS)         <= RONLY;
  registersAccesMode(REG_ADDR)           <= RW;
  registersAccesMode(REG_WRITE_DATA + 0) <= RW;
  registersAccesMode(REG_WRITE_DATA + 1) <= RW;
  registersAccesMode(REG_WRITE_DATA + 2) <= RW;
  registersAccesMode(REG_WRITE_DATA + 3) <= RW;
  registersAccesMode(REG_READ_DATA + 0)  <= RONLY;
  registersAccesMode(REG_READ_DATA + 1)  <= RONLY;
  registersAccesMode(REG_READ_DATA + 2)  <= RONLY;
  registersAccesMode(REG_READ_DATA + 3)  <= RONLY;

  ---------------------------------------------------------  
  -- Periph Bus Manager                                  --
  ---------------------------------------------------------
  PeriphBusManager_P : process(PeriphClk, PeriphRstN)
  begin
    if (PeriphRstN = '0') then

      --Register Initalization
      registersRW(REG_CONTROL)      <= b"00000000";
      registersRW(REG_ADDR)         <= x"00";
      registersRW(REG_WRITE_DATA+0) <= x"00";
      registersRW(REG_WRITE_DATA+1) <= x"00";
      registersRW(REG_WRITE_DATA+2) <= x"00";
      registersRW(REG_WRITE_DATA+3) <= x"00";

      --Data Initialization
      PeriphDataOut <= (others => '0');
      
    elsif rising_edge(PeriphClk) then
      if PeriphCeN = '0' then
        if PeriphWeN = '0' then
          if registersAccesMode(to_integer(PeriphAddr)) = '0' then
            registersRW(to_integer(PeriphAddr)) <= PeriphDataIn;
          end if;
        else
          if registersAccesMode(to_integer(PeriphAddr)) = '0' then
            PeriphDataOut <= registersRW(to_integer(PeriphAddr));
          else
            PeriphDataOut <= registersRONLY(to_integer(PeriphAddr));
          end if;
        end if;
      else
        PeriphDataOut <= (others => '0');
      end if;

      regControl_d <= registersRW(REG_CONTROL);
      
    end if;
  end process PeriphBusManager_P;

  --Command Detection
  i2cStartWrite <= registersRW(REG_CONTROL)(0) and not regControl_d(0);
  i2cStartRead  <= registersRW(REG_CONTROL)(1) and not regControl_d(1);


  ---------------------------------------------------------  
  -- Physical Manager                                    --
  ---------------------------------------------------------
  PhysicalManager_P : process(PeriphClk, PeriphRstN)
  begin
    if (PeriphRstN = '0') then

      physicalState     <= IDLE;
      nextPhysicalState <= IDLE;

      registersRONLY(REG_READ_DATA+0) <= x"00";
      registersRONLY(REG_READ_DATA+1) <= x"00";
      registersRONLY(REG_READ_DATA+2) <= x"00";
      registersRONLY(REG_READ_DATA+3) <= x"00";
      registersRONLY(REG_STATUS) <= (others => '0');

      i2cAccesSize <= (others => '0');
      i2cWriteOnGoing <= '0';
      i2cReadOnGoing  <= '0';
      
      i2cAckError <= '0';
      PeriphAckN  <= '1';
      
    elsif rising_edge(PeriphClk) then
      case physicalState is
        -- Start I2c Transaction
        when START =>
          logOperation      <= I2C_START;
          logEnable         <= '1';
          physicalState     <= WAIT_FOR_DONE;
          nextPhysicalState <= WRITE_ADDR;

          -- Stop I2c Transation
        when STOP =>
          logOperation      <= I2C_STOP;
          logEnable         <= '1';
          physicalState     <= WAIT_FOR_DONE;
          nextPhysicalState <= IDLE;


          -- Write Slave Addr on Bus
        when WRITE_ADDR=>
          logOperation  <= I2C_WRITE_DATA;
          logEnable     <= '1';
          logDataIn     <= registersRW(REG_ADDR);
          physicalState <= WAIT_FOR_DONE;

          if i2cWriteOnGoing = '1' then
            nextPhysicalState <= WRITE_DATA;
          elsif i2cReadOnGoing = '1' then
            nextPhysicalState <= READ_DATA;
          else
            nextPhysicalState <= STOP;
          end if;

          -- Write Data On Bus
        when WRITE_DATA=>
          logOperation  <= I2C_WRITE_DATA;
          logEnable     <= '1';
          logDataIn     <= registersRW(REG_WRITE_DATA+to_integer(i2cAccesCpt));
          physicalState <= WAIT_FOR_DONE;

          i2cAccesCpt <= i2cAccesCpt+1;

          if i2cAccesCpt /= i2cAccesSize then
            nextPhysicalState <= WRITE_DATA;
          else
            nextPhysicalState <= STOP;
          end if;


          -- Read Data On Bus
        when READ_DATA=>
          if i2cAccesCpt /= i2cAccesSize then
            logOperation <= I2C_READ_DATA_ACK;
          else
            logOperation <= I2C_READ_DATA_NACK;
          end if;

          logEnable     <= '1';
          physicalState <= WAIT_FOR_DONE;

          i2cAccesCpt <= i2cAccesCpt+1;

          if i2cAccesCpt /= i2cAccesSize then
            nextPhysicalState <= READ_DATA;
          else
            nextPhysicalState <= STOP;
          end if;


          -- Wait Transaction to be done  
        when WAIT_FOR_DONE=>
          
          logEnable <= '0';
          if logDone = '1' then
            physicalState <= nextPhysicalState;
            if physicalState = READ_DATA then
              registersRONLY(REG_READ_DATA+to_integer(i2cAccesCpt)) <= LogDataOut;
            elsif physicalState = WRITE_DATA then
              i2cAckError <= i2cAckError or LogSlaveAck;
            end if;

            if nextPhysicalState = IDLE then
              PeriphAckN <= '0';
            end if;
            
          end if;

          -- Idle
        when others =>
          i2cWriteOnGoing <= i2cStartWrite;
          i2cReadOnGoing  <= i2cStartRead;
          i2cAccesSize  <= registersRW(REG_CONTROL)(3 downto 2);

          if (i2cStartWrite or i2cStartRead) = '1' then
            physicalState <= START;
          else
            physicalState <= IDLE;
          end if;

          if i2cAckErrorClear = '1' then
            i2cAckError <= '0';
          end if;

          i2cAccesCpt <= (others => '0');
          PeriphAckN  <= '1';
          
      end case;

  --Fill Status Register
  registersRONLY(REG_STATUS)(7 downto 5) <= (others => '0');
  registersRONLY(REG_STATUS)(4)          <= i2cAckError;
  registersRONLY(REG_STATUS)(3)          <= '0';
  registersRONLY(REG_STATUS)(2)          <= i2cWriteOnGoing or i2cReadOnGoing;
  registersRONLY(REG_STATUS)(1)          <= not i2cReadOnGoing;
  registersRONLY(REG_STATUS)(0)          <= not i2cWriteOnGoing;  
      
    end if;
  end process PhysicalManager_P;

 

  ---------------------------------------------------------  
  -- Physical Master                                     --
  ---------------------------------------------------------
  I2CPhysicalMaster_1 : I2CPhysicalMaster
    generic map (
      FCLK  => FCLK,
      SPEED => SPEED)
    port map (
      Clk          => PeriphClk,
      RstN         => PeriphRstN,
      PhysSclOut   => PhysSclOut,
      PhysSdaInOut => PhysSdaInOut,
      LogEnable    => logEnable,
      LogOperation => logOperation,
      LogDone      => logDone,
      LogDataIn    => logDataInStd,
      LogDataOut   => logDataOutStd,
      LogSlaveAck  => logSlaveAck);

  logDataInStd <= std_logic_vector(logDataIn);
  logDataOut   <= unsigned(logDataOutStd);


end Rtl;
