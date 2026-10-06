#pragma once

// Project-local, zero-runtime markers for the standalone Vexgraph build graph.
#define DEFINITION _Static_assert(1, "@Definition");
#define OVERVIEW _Static_assert(1, "@Overview");

;;DEFINITION
/* The graph can describe its blueprint without linking to the engine whose
 * sources it builds. These macros perform no runtime work.
 */
;;OVERVIEW
/* MODULE: build-graph annotations. PUBLIC MACROS: DEFINITION and OVERVIEW.
 * Both expand to compile-time assertions; no class, allocation or runtime API.
 */
