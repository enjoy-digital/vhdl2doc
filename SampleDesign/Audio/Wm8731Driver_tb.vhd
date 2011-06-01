-------------------------------------------------------------------------------
-- Title      : Testbench for design "Wm8731Driver"
-- Project    : 
-------------------------------------------------------------------------------
-- File       : Wm8731Driver_tb.vhd
-- Author     : 
-- Company    : 
-- Created    : 2011-05-08
-- Last update: 2011-05-08
-- Platform   : 
-- Standard   : VHDL'87
-------------------------------------------------------------------------------
-- Description: 
-------------------------------------------------------------------------------
-- Copyright (c) 2011 
-------------------------------------------------------------------------------
-- Revisions  :
-- Date        Version  Author  Description
-- 2011-05-08  1.0      Florent	Created
-------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-------------------------------------------------------------------------------

entity Wm8731Driver_tb is

end Wm8731Driver_tb;

-------------------------------------------------------------------------------

architecture Tb of Wm8731Driver_tb is

  component Wm8731Driver
    port (
      Clk        : in    std_logic;
      RstN       : in    std_logic;
      AudioData  : in    unsigned(15 downto 0);
      I2cScl     : out   std_logic;
      I2cSda     : inout std_logic;
      I2sAdcLrCk : inout std_logic;
      I2sAdcDat  : in    std_logic;
      I2sDacLrCk : inout std_logic;
      I2sDacDat  : out   std_logic;
      I2sBClk    : inout std_logic;
      I2sXCk     : out   std_logic);
  end component;

  -- component ports
  signal Clk        : std_logic := '1';
  signal RstN       : std_logic := '0';
  signal AudioData  : unsigned(15 downto 0);
  signal I2cScl     : std_logic;
  signal I2cSda     : std_logic;
  signal I2sAdcLrCk : std_logic;
  signal I2sAdcDat  : std_logic;
  signal I2sDacLrCk : std_logic;
  signal I2sDacDat  : std_logic;
  signal I2sBClk    : std_logic;
  signal I2sXCk     : std_logic;



begin  -- Tb

  -- component instantiation
  DUT: Wm8731Driver
    port map (
      Clk        => Clk,
      RstN       => RstN,
      AudioData  => AudioData,
      I2cScl     => I2cScl,
      I2cSda     => I2cSda,
      I2sAdcLrCk => I2sAdcLrCk,
      I2sAdcDat  => I2sAdcDat,
      I2sDacLrCk => I2sDacLrCk,
      I2sDacDat  => I2sDacDat,
      I2sBClk    => I2sBClk,
      I2sXCk     => I2sXCk);

  -- clock generation
  Clk  <= not Clk after 35.5 ns;
  RstN <= '1' after 10 us;
  I2cSda <= 'H';

  

end Tb;

-------------------------------------------------------------------------------

configuration Wm8731Driver_tb_Tb_cfg of Wm8731Driver_tb is
  for Tb
  end for;
end Wm8731Driver_tb_Tb_cfg;

-------------------------------------------------------------------------------
