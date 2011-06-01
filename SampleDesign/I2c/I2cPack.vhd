--=============================================================================--
--   Title & version       : I2cPack
--   Company               : EnjoyDigital
--   Filename              : I2cPack.vhd
--   Date (yyyy-mm-dd)     : 07/05/2011
--   Purpose               : I2C Constants,Type,Functions
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

--============================================================================--
--                             Package
--============================================================================--
--* @link     [package] [I2cPack]
--* @brief    I2c Constants,Type,Functions Package
-------------------------------------------------------------------------------
package I2cPack is

  --===================================--
  -- Constants Declaration
  --===================================--
  constant VOID      : std_logic_vector(2 downto 0) := b"000";
  constant R0        : std_logic_vector(2 downto 0) := b"000";
  constant R1        : std_logic_vector(2 downto 0) := b"001";
  constant R2        : std_logic_vector(2 downto 0) := b"010";
  constant R3        : std_logic_vector(2 downto 0) := b"011";
  constant R4        : std_logic_vector(2 downto 0) := b"100";
  constant R5        : std_logic_vector(2 downto 0) := b"101";
  constant R6        : std_logic_vector(2 downto 0) := b"110";
  constant R7        : std_logic_vector(2 downto 0) := b"111";
  constant ALWAYS    : std_logic_vector(2 downto 0) := b"000";
  constant EQUAL     : std_logic_vector(2 downto 0) := b"001";
  constant NOT_EQUAL : std_logic_vector(2 downto 0) := b"010";

  --Register Number
  constant REGISTER_NB   : natural := 16;
  constant REGISTER_SIZE : natural :=  8;

  --Control
  constant REG_CONTROL : natural := 0;
  constant REG_STATUS  : natural := 1;
  constant REG_ADDR    : natural := 2;

  --Data Buffering
  constant REG_WRITE_DATA : natural := 8;
  constant REG_READ_DATA  : natural := 12;

  --R/W Mode
  constant RW    : std_logic := '0';
  constant RONLY : std_logic := '1';
  
  --===================================--
  -- Types Declaration
  --===================================--
  -- I2C Physical Atomic Operations
  type I2C_PHYSICAL_AT_OP is (I2C_START,
                              I2C_RESTART,
                              I2C_STOP,
                              I2C_WRITE_DATA,
                              I2C_READ_DATA_ACK,
                              I2C_READ_DATA_NACK);

  --===================================--
  -- Components Declaration
  --===================================--
  -- Insert Component Here

  --===================================--
  -- Functions Declaration
  --===================================--
  -- Integer2Std_Logic_Vector
  function int2std_8b(value : natural range 0 to 255) return std_logic_vector;
  function int2std_4b(value : natural range 0 to 15)  return std_logic_vector;

  -- I2C_PHYSICAL_AT_OP <--> Std_Logic_Vector
  function atOpe2Std(value : std_logic_vector(2 downto 0)) return I2C_PHYSICAL_AT_OP;
  function std2AtOpe(value : I2C_PHYSICAL_AT_OP) return std_logic_vector;

end I2cPack;

--============================================================================--
--                                 Body
--============================================================================--
package body I2cPack is

  -- Integer2Std_Logic_Vector
  function int2std_8b(value : natural range 0 to 255) return std_logic_vector is
  begin
    return std_logic_vector(to_unsigned(value, 8));
  end function int2std_8b;

  -- Integer2Std_Logic_Vector
  function int2std_4b(value : natural range 0 to 15) return std_logic_vector is
  begin
    return std_logic_vector(to_unsigned(value, 4));
  end function int2std_4b;

  -- Std_Logic_Vector --> I2C_PHYSICAL_AT_OP
  function atOpe2Std(value : std_logic_vector(2 downto 0)) return I2C_PHYSICAL_AT_OP is
    variable result : I2C_PHYSICAL_AT_OP;
  begin
    case value is
      when b"000" => result := I2C_START;           -- 0
      when b"001" => result := I2C_RESTART;         -- 1
      when b"010" => result := I2C_STOP;            -- 2
      when b"011" => result := I2C_WRITE_DATA;      -- 3
      when b"100" => result := I2C_READ_DATA_ACK;   -- 4
      when others => result := I2C_READ_DATA_NACK;  -- 5
    end case;
    return result;
  end function atOpe2Std;

  -- I2C_PHYSICAL_AT_OP <--> Std_Logic_Vector
  function std2AtOpe(value : I2C_PHYSICAL_AT_OP) return std_logic_vector is
    variable result : std_logic_vector(2 downto 0);
  begin
    case value is
      when I2C_START          => result := b"000";  -- 0
      when I2C_RESTART        => result := b"001";  -- 1
      when I2C_STOP           => result := b"010";  -- 2
      when I2C_WRITE_DATA     => result := b"011";  -- 3
      when I2C_READ_DATA_ACK  => result := b"100";  -- 4
      when I2C_READ_DATA_NACK => result := b"101";  -- 5
    end case;
    return result;
  end function std2AtOpe;

end I2cPack;
