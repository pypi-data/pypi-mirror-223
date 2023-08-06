/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
define(["@jupyter-widgets/base"], (__WEBPACK_EXTERNAL_MODULE__jupyter_widgets_base__) => { return /******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./src/plugin.ts":
/*!***********************!*\
  !*** ./src/plugin.ts ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (__WEBPACK_DEFAULT_EXPORT__)\n/* harmony export */ });\n/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ \"@jupyter-widgets/base\");\n/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ \"./src/widget.ts\");\n/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_widget__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./version */ \"./src/version.ts\");\n// For licensing see accompanying LICENSE file.\n// Copyright (C) 2023 Apple Inc. All Rights Reserved.\n\n\n\nconst EXTENSION_ID = 'symphony-vega:plugin';\n/**\n * The example plugin.\n */\nconst examplePlugin = {\n    id: EXTENSION_ID,\n    requires: [_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.IJupyterWidgetRegistry],\n    activate: activateWidgetExtension,\n    autoStart: true,\n};\n// the \"as unknown as ...\" typecast above is solely to support JupyterLab 1\n// and 2 in the same codebase and should be removed when we migrate to Lumino.\n/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (examplePlugin);\n/**\n * Activate the widget extension.\n */\nfunction activateWidgetExtension(app, registry) {\n    registry.registerWidget({\n        name: _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_NAME,\n        version: _version__WEBPACK_IMPORTED_MODULE_2__.MODULE_VERSION,\n        exports: _widget__WEBPACK_IMPORTED_MODULE_1__,\n    });\n}\n\n\n//# sourceURL=webpack://symphony-vega/./src/plugin.ts?");

/***/ }),

/***/ "./src/version.ts":
/*!************************!*\
  !*** ./src/version.ts ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   MODULE_NAME: () => (/* binding */ MODULE_NAME),\n/* harmony export */   MODULE_VERSION: () => (/* binding */ MODULE_VERSION)\n/* harmony export */ });\n// For licensing see accompanying LICENSE file.\n// Copyright (C) 2023 Apple Inc. All Rights Reserved.\n// eslint-disable-next-line @typescript-eslint/no-var-requires\nconst data = __webpack_require__(/*! ../package.json */ \"./package.json\");\n/**\n * The _model_module_version/_view_module_version this package implements.\n *\n * The html widget manager assumes that this is the same as the npm package\n * version number.\n */\nconst MODULE_VERSION = data.version;\n/*\n * The current package name.\n */\nconst MODULE_NAME = data.name;\n\n\n//# sourceURL=webpack://symphony-vega/./src/version.ts?");

/***/ }),

/***/ "./src/widget.ts":
/*!***********************!*\
  !*** ./src/widget.ts ***!
  \***********************/
/***/ (() => {

eval("throw new Error(\"Module build failed (from ../../node_modules/ts-loader/index.js):\\nError: TypeScript emitted no output for /Users/fredhohman/Github/apple/ml-symphony/widgets/symphony_vega/src/widget.ts.\\n    at makeSourceMapAndFinish (/Users/fredhohman/Github/apple/ml-symphony/node_modules/ts-loader/dist/index.js:52:18)\\n    at successLoader (/Users/fredhohman/Github/apple/ml-symphony/node_modules/ts-loader/dist/index.js:39:5)\\n    at Object.loader (/Users/fredhohman/Github/apple/ml-symphony/node_modules/ts-loader/dist/index.js:22:5)\");\n\n//# sourceURL=webpack://symphony-vega/./src/widget.ts?");

/***/ }),

/***/ "@jupyter-widgets/base":
/*!****************************************!*\
  !*** external "@jupyter-widgets/base" ***!
  \****************************************/
/***/ ((module) => {

"use strict";
module.exports = __WEBPACK_EXTERNAL_MODULE__jupyter_widgets_base__;

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
eval("module.exports = JSON.parse('{\"name\":\"symphony-vega\",\"version\":\"1.0.0\",\"description\":\"A component that can be passed vega specs to be rendered.\",\"private\":true,\"keywords\":[\"jupyter\",\"jupyterlab\",\"jupyterlab-extension\",\"widgets\"],\"files\":[\"lib/**/*.js\",\"dist/*.js\",\"standalone/*\"],\"main\":\"lib/index.js\",\"types\":\"lib/index.d.ts\",\"homepage\":\"https://github.com/apple/ml-symphony\",\"bugs\":{\"url\":\"https://github.com/apple/ml-symphony/issues\"},\"author\":\"Apple\",\"repository\":{\"type\":\"git\",\"url\":\"https://github.com/apple/ml-symphony\"},\"scripts\":{\"build\":\"webpack --mode=development --progress && jupyter labextension build --development=True .\",\"build:prod\":\"webpack --mode=production && jupyter labextension build .\",\"clean\":\"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension && yarn run clean:standalone\",\"clean:lib\":\"rimraf lib\",\"clean:labextension\":\"rimraf symphony_vega/labextension\",\"clean:nbextension\":\"rimraf symphony_vega/nbextension/static/index.js\",\"clean:standalone\":\"rimraf symphony_vega/standalone\",\"lint\":\"eslint . --ext .ts,.tsx,.svelte --fix\",\"lint:check\":\"eslint . --ext .ts,.tsx,.svelte\",\"prepack\":\"yarn run build:prod\",\"watch\":\"yarn run watch:nbextension\",\"watch:nbextension\":\"webpack --watch --mode=development --progress\",\"watch:labextension\":\"jupyter labextension watch .\",\"dev\":\"yarn run watch & python -m http.server --directory ./symphony_vega/standalone 8082\"},\"dependencies\":{\"@apple/symphony-lib\":\"^1.0.0\",\"@jupyter-widgets/base\":\"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0\",\"arquero\":\"^4.7.2\"},\"devDependencies\":{\"@fullhuman/postcss-purgecss\":\"^4.0.3\",\"@jupyterlab/builder\":\"^3.0.9\",\"@phosphor/application\":\"^1.6.0\",\"@phosphor/widgets\":\"^1.6.0\",\"@tailwindcss/forms\":\"^0.3.2\",\"@tsconfig/svelte\":\"^2.0.1\",\"@types/webpack-env\":\"^1.13.6\",\"@typescript-eslint/eslint-plugin\":\"^4.21.0\",\"@typescript-eslint/parser\":\"^4.21.0\",\"@webpack-cli/serve\":\"^1.2.2\",\"autoprefixer\":\"^10.2.5\",\"commitizen\":\"^4.2.4\",\"css-loader\":\"^6.3.0\",\"css-minimizer-webpack-plugin\":\"^3.0.1\",\"cz-conventional-changelog\":\"^3.3.0\",\"eslint\":\"^7.4.0\",\"eslint-config-prettier\":\"^8.1.0\",\"eslint-plugin-prettier\":\"^4.0.0\",\"mini-css-extract-plugin\":\"^2.3.0\",\"mkdirp\":\"^1.0.4\",\"postcss\":\"^8.2.10\",\"postcss-extend\":\"^1.0.5\",\"postcss-import\":\"^14.0.1\",\"postcss-load-config\":\"^3.0.1\",\"postcss-loader\":\"^6.1.0\",\"precss\":\"^4.0.0\",\"prettier\":\"^2.0.5\",\"purgecss-from-svelte\":\"^2.0.2\",\"rimraf\":\"^3.0.2\",\"source-map-loader\":\"^3.0.0\",\"style-loader\":\"^3.2.1\",\"svelte\":\"^3.1.4\",\"svelte-loader\":\"^3.1.1\",\"svelte-preprocess\":\"^4.7.0\",\"tailwindcss\":\"^2.1.1\",\"ts-loader\":\"^9.1.0\",\"typescript\":\"~4.4.3\",\"webpack\":\"^5.30.0\",\"webpack-cli\":\"^4.6.0\",\"webpack-dev-server\":\"^4.2.1\",\"yarn-run-all\":\"^3.1.1\"},\"jupyterlab\":{\"extension\":\"lib/index\",\"outputDir\":\"symphony_vega/labextension/\",\"sharedPackages\":{\"@jupyter-widgets/base\":{\"bundled\":false,\"singleton\":true}}},\"config\":{\"commitizen\":{\"path\":\"./node_modules/cz-conventional-changelog\"}}}');\n\n//# sourceURL=webpack://symphony-vega/./package.json?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./src/plugin.ts");
/******/ 	
/******/ 	return __webpack_exports__;
/******/ })()
;
});;