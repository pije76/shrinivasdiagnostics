import { babel } from '@rollup/plugin-babel';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import { terser } from 'rollup-plugin-terser';
import license from 'rollup-plugin-license';

import pkg from './package.json';

const dist = 'dist';
const license_banner = {
    banner: `
     ${pkg.title || pkg.name} - v${pkg.version}
     ${pkg.description}
     ${pkg.homepage}

     Made by ${pkg.author}
     Under ${pkg.license} License
    `
};

export default [
    {
        input: './src/index.js',
        output: {
            file: `${dist}/js/simpledropit.cjs.js`,
            format: 'cjs'
        },
        plugins: [
            babel({
                exclude: ['/**/node_modules/**/']
            }),
            resolve(),
            commonjs(),
            license(license_banner)
        ]
    },
    {
        input: './src/index.js',
        external: id => {
            if (
              Object.keys(pkg.dependencies).find(dep => id === dep) ||
              id.match(/(core-js).+/)
            ) {
              return true;
            }
      
            return false;
        },
        output: {
            file: `${dist}/js/simpledropit.esm.js`,
            format: 'esm'
        },
        plugins: [
            babel({
                exclude: ['/**/node_modules/**/']
            }),
            license(license_banner)
        ]
    },
    {
        input: './src/index.js',
        external: id => {
            if (
              Object.keys(pkg.dependencies).find(dep => id === dep) ||
              id.match(/(core-js).+/)
            ) {
              return true;
            }
      
            return false;
        },
        output: [
            {
                file: `${dist}/js/simpledropit.js`,
                format: 'umd',
                name: 'SimpleDropit'
            },
        ],
        plugins: [
            babel({
                exclude: ['/**/node_modules/**/']
            }),
            resolve(),
            commonjs(),
            license(license_banner)
        ]
    },
    {
        input: './src/index.js',
        output: {
            file: `${dist}/js/simpledropit.min.js`,
            format: 'umd',
            name: 'SimpleDropit',
        },
        plugins: [
            babel({
                exclude: ['/**/node_modules/**/']
            }),
            resolve(),
            commonjs,
            terser(),
            license(license_banner)
        ]
    }
];