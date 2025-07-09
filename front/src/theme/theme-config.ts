import type { CommonColors } from '@mui/material/styles';

import type { ThemeCssVariables } from './types';
import type { PaletteColorNoChannels } from './core/palette';

// ----------------------------------------------------------------------

type ThemeConfig = {
  classesPrefix: string;
  cssVariables: ThemeCssVariables;
  fontFamily: Record<'primary' | 'secondary', string>;
  palette: Record<
    'primary' | 'secondary' | 'info' | 'success' | 'warning' | 'error',
    PaletteColorNoChannels
  > & {
    common: Pick<CommonColors, 'black' | 'white'>;
    grey: Record<
      '50' | '100' | '200' | '300' | '400' | '500' | '600' | '700' | '800' | '900',
      string
    >;
  };
};

export const themeConfig: ThemeConfig = {
  /** **************************************
   * Base
   *************************************** */
  classesPrefix: 'minimal',
  /** **************************************
   * Typography
   *************************************** */
  fontFamily: {
    primary: 'Source Sans Pro',
    secondary: 'Source Sans Pro',
  },
  /** **************************************
   * Palette
   *************************************** */
  palette: {
  primary: {
    lighter: '#6d597a', // Chinese Violet (lighter variant)
    light: '#b56576',   // China Rose
    main: '#355070',    // YInMn Blue
    dark: '#6d597a',    // Chinese Violet (repeated for contrast)
    darker: '#b56576',  // China Rose (deepest)
    contrastText: '#FFFFFF',
  },
  secondary: {
    lighter: '#eaac8b', // Buff
    light: '#e56b6f',   // Light Coral
    main: '#eaac8b',    // Buff
    dark: '#b56576',    // China Rose
    darker: '#6d597a',  // Chinese Violet
    contrastText: '#000000',
  },
  info: {
    lighter: '#fbeaea',
    light: '#f3bfbf',
    main: '#e56b6f',
    dark: '#b4484b',
    darker: '#8b2e31',
    contrastText: '#FFFFFF',
  },
  success: {
    lighter: '#edf7f2',
    light: '#b6dfc4',
    main: '#74c69d',
    dark: '#40916c',
    darker: '#1b4332',
    contrastText: '#FFFFFF',
  },
  warning: {
    lighter: '#fff4e6',
    light: '#ffd8a8',
    main: '#ffa94d',
    dark: '#e67700',
    darker: '#ad5700',
    contrastText: '#000000',
  },
  error: {
    lighter: '#ffe3e3',
    light: '#ff6b6b',
    main: '#fa5252',
    dark: '#c92a2a',
    darker: '#a51111',
    contrastText: '#FFFFFF',
  },
  grey: {
    '50': '#fafafa',
    '100': '#f4f4f4',
    '200': '#e0e0e0',
    '300': '#c2c2c2',
    '400': '#a3a3a3',
    '500': '#858585',
    '600': '#666666',
    '700': '#4d4d4d',
    '800': '#333333',
    '900': '#1a1a1a',
  },
  common: { black: '#000000', white: '#FFFFFF' },
  },
  /** **************************************
   * Css variables
   *************************************** */
  cssVariables: {
    cssVarPrefix: '',
    colorSchemeSelector: 'data-color-scheme',
  },
};
