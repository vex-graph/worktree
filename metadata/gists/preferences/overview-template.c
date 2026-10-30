/* overview-template.c — template for a self-contained .c (Living Documentation Law) */

#include "annotation/definition.h"
#include "annotation/overview.h"

;;DEFINITION
/**
 * ============================================================================
 * DEFINITION: ClassName
 * ============================================================================
 * <architectural raison d'etre: why this class exists, its role in the tier,
 * memory layout, mechanics, concurrency, relationships to adjacent R tiers>
 * ============================================================================
 */

;;OVERVIEW
/**
 * ============================================================================
 * CLASS: ClassName (path/to/classname.c)
 * ============================================================================
 * <one-paragraph structural summary>
 *
 * STRUCT FIELDS (Mirroring path/to/classname.h):
 * ----------------------------------------------------------------------------
 *   <type> <name>  — <one-line role>
 *   ...
 *
 * PRIVATE HELPERS:
 * ----------------------------------------------------------------------------
 *   <helperName>  — <full field list + role>
 *
 * SLOT RECORDS:
 * ----------------------------------------------------------------------------
 *   <SlotName>  — <fields>
 *
 * FUNCTION REGISTRY:
 * ----------------------------------------------------------------------------
 * Constructors:
 *   - ClassName(...)
 *
 * Core operations:
 *   - ClassName_doThing(...)
 *
 * Setters:
 *   - ClassName_setProp(...)
 *
 * Getters:
 *   - ClassName_getProp(...)
 *
 * Projections:
 *   - ClassName_toString(...)
 *
 * Lifecycle:
 *   - ClassName_free(...)
 *
 * ADMISSION / NULL / FAILURE / OWNERSHIP CONTRACT:
 * ----------------------------------------------------------------------------
 *   <null self returns safe default; failure preserves state; ownership rules>
 * ============================================================================
 */

/* implementation follows */
