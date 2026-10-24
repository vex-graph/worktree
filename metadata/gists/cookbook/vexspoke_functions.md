# Vexspoke Function Calls

This page is a bare call reference for Vexspoke's callable APIs. Each example
shows the public call spelling inside one `main`. It is not a recipe, tutorial,
or correctness test; read the owning header for contracts and use the test suite
for behavior proof. The universal Value Return Law forbids caller-provided
destinations: examples below that still show output parameters are legacy
signatures in the current source, not the desired API, and remain migration gaps.

## Arithmetic overload functions (overload.h)

The two-argument forms return scalar or vector values directly. The three-
argument destination forms remain Value Return Law migration gaps.

```c
#include "c23/overload.h"

int main(void)
{
    float sum = add(1.5f, 2.5f);
    float difference = sub(5.0f, 2.0f);
    float product = mul(3.0f, 4.0f);
    float quotient = div(8.0f, 2.0f);
    return 0;
}
```

Vexspoke is R2. Memory and IO/NIO implementations belong to Relational Engine;
Vexspoke contains no `io/` or `nio/` implementation. Graphical rendering belongs
to Graphvex, host windows to Hotcwap, and managed terminal UI to Determinant.

## Random class (random.c)

```c
#include "util/random.h"

int main(void)
{
    Random *random = Random(90210u);
    Random *systemRandom = Random_system();
    Random *secondEngine = Random(90210u, RANDOM_ENGINE_PCG);
    RandomEngine engine = Random_engine(random);
    uint64_t next = Random_nextLong(random);
    int32_t nextInt = Random_nextInt(random);
    float nextFloat = Random_nextFloat(random);
    double sample = Random_nextDouble(random);
    float ndcSample = Random_nextNDCFloat(random);
    char nextChar = Random_nextChar(random);
    bool weightAccepted = Random_getWeight(random, 2u, 5u);
    Probable *probable = nullptr;
    ProbableObjects *weightedObjects = nullptr;
    uintptr_t sampledItem = Random_sample(random, probable);
    uintptr_t sampledObjects = Random_probablePool(random, weightedObjects);
    Random_free(secondEngine);
    Random_free(random);
    Random_free(systemRandom);
    return 0;
}
```

## Vec3 class (vec3.c)

`Vec3_copy`, `Vec3_toFrame`, `Vec3_add`, `Vec3_sub`, `Vec3_mul`, `Vec3_div`,
`Vec3_cross`, `Vec3_normalize`, `Vec3_fastNormalize`, `Vec3_project`,
`Vec3_reflect`, `Vec3_clamp`, `Vec3_abs`, and `Vec3_lerp` still require caller
destinations and are omitted under Value Return Law. The scalar getters return
values directly and are assigned below.

```c
#include "lang/vec3.h"

int main(void)
{
    Vec3 *direction = Vec3(3.0f, 4.0f, 0.0f);
    Vec3 *unitDirection = Vec3();
    Vec3 *thirdVector = Vec3(1.0f, 0.0f, 0.0f);
    CoordFrame frame = COORD_FRAME_Y_UP_LEFT;
    float right = Vec3_getRight(direction);
    Vec3_setRight(direction, 3.0f);
    float left = Vec3_getLeft(direction);
    Vec3_setLeft(direction, -3.0f);
    float up = Vec3_getUp(direction);
    Vec3_setUp(direction, 4.0f);
    float down = Vec3_getDown(direction);
    Vec3_setDown(direction, -4.0f);
    float front = Vec3_getFront(direction);
    Vec3_setFront(direction, 0.0f);
    float back = Vec3_getBack(direction);
    Vec3_setBack(direction, 0.0f);
    CoordFrame currentFrame = Vec3_getFrame(direction);
    Vec3_setFrame(direction, frame);
    float x = Vec3_getX(direction);
    Vec3_setX(direction, 3.0f);
    float y = Vec3_getY(direction);
    Vec3_setY(direction, 4.0f);
    float z = Vec3_getZ(direction);
    Vec3_setZ(direction, 0.0f);
    float frameX = Vec3_getXInFrame(direction, frame);
    float frameY = Vec3_getYInFrame(direction, frame);
    float frameZ = Vec3_getZInFrame(direction, frame);
    Vec3_set(direction, 3.0f, 4.0f, 0.0f);
    float dot = Vec3_dot(direction, thirdVector);
    float lengthSquared = Vec3_lengthSquared(direction);
    float length = Vec3_length(direction);
    float distance = Vec3_distance(direction, thirdVector);
    float angle = Vec3_angle(direction, thirdVector);
    Vec3_free(unitDirection);
    Vec3_free(thirdVector);
    Vec3_free(direction);
    return 0;
}
```

## Point class (point.c)

`Point_copy`, `Point_add`, `Point_sub`, `Point_scale`, `Point_negate`,
`Point_min`, and `Point_max` still require caller-provided destinations and are
Value Return Law migration gaps. Scalar getters and metrics return values
directly and are shown below.

```c
#include "lang/point/point.h"

int main(void)
{
    Point *cursor = Point(120, 80);
    Point_setX(cursor, 124);
    Point *origin = Point();
    Point_setY(cursor, 80);
    Point_set(cursor, 124, 80);
    int32_t x = Point_getX(cursor);
    int32_t y = Point_getY(cursor);
    int64_t squaredDistance = Point_distanceSquared(cursor, origin);
    int64_t manhattanDistance = Point_manhattanDistance(cursor, origin);
    double distance = Point_distance(cursor, origin);
    bool equal = Point_equals(cursor, origin);
    Point_free(origin);
    Point_free(cursor);
    return 0;
}
```

## Rectangle class (rectangle.c)

`Rectangle_copy`, `Rectangle_translate`, `Rectangle_inflate`,
`Rectangle_inset`, `Rectangle_intersection`, and `Rectangle_merge` still require
caller-provided destinations and are Value Return Law migration gaps. Scalar
getters and predicates return values directly and are shown below.

```c
#include "lang/rect/rectangle.h"

int main(void)
{
    Rectangle *bounds = Rectangle(100.0f, 50.0f, 240.0f, 120.0f);
    Rectangle *other = Rectangle();
    Rectangle_setX(bounds, 100.0f);
    Rectangle_setY(bounds, 50.0f);
    Rectangle_setWidth(bounds, 240.0f);
    Rectangle_setHeight(bounds, 120.0f);
    Rectangle_set(bounds, 100.0f, 50.0f, 240.0f, 120.0f);
    float x = Rectangle_getX(bounds);
    float y = Rectangle_getY(bounds);
    float width = Rectangle_getWidth(bounds);
    float height = Rectangle_getHeight(bounds);
    float left = Rectangle_getLeft(bounds);
    float top = Rectangle_getTop(bounds);
    float right = Rectangle_getRight(bounds);
    float bottom = Rectangle_getBottom(bounds);
    bool empty = Rectangle_isEmpty(bounds);
    bool containsPoint = Rectangle_containsPoint(bounds, 120.0f, 80.0f);
    bool containsRect = Rectangle_containsRect(bounds, other);
    bool intersects = Rectangle_intersects(bounds, other);
    bool equal = Rectangle_equals(bounds, other);
    Rectangle_free(other);
    Rectangle_free(bounds);
    return 0;
}
```

## Mat4 class (mat4.c)

`Mat4_identityAlloc` is a legacy factory outside the preferred `Mat4(...)`
constructor macro. `Mat4_copy`, `Mat4_multiply`, `Mat4_transpose`,
`Mat4_createTransformationMatrix`, `Mat4_createTransformationMatrix2D`,
`Mat4_createViewMatrix`, `Mat4_translate`, `Mat4_scale`, `Mat4_rotate`,
`Mat4_perspective`, `Mat4_perspectiveVulkan`, `Mat4_orthographic`,
`Mat4_lookAt`, `Mat4_transform`, and `Mat4_transformVec3` all write through
caller-provided destinations and are Value Return Law migration gaps.

```c
#include "lang/mat4.h"

int main(void)
{
    Mat4 *matrix = Mat4();
    Mat4 *other = Mat4();
    Vec3 *vector3 = Vec3();
    Vec4 *vector4 = Vec4();
    float scalar = 0.0f;
    float value = Mat4_get(matrix, 0, 0);
    Mat4_set(matrix, 0, 0, 1.0f);
    float rawValue = Mat4_getRaw(matrix, 0);
    Mat4_setRaw(matrix, 0, 1.0f);
    Mat4_zero(matrix);
    Mat4_identity(matrix);
    scalar = value;


    Mat4_free(other);
    Mat4_free(matrix);
    Vec4_free(vector4);
    Vec3_free(vector3);
    return 0;
}
```

## Vec2 class (vec2.c)

`Vec2_copy`, `Vec2_add`, `Vec2_sub`, `Vec2_mul`, `Vec2_div`,
`Vec2_normalize`, `Vec2_perpendicular`, and `Vec2_lerp` still require caller
destinations and are omitted under Value Return Law.

```c
#include "lang/vec2/vec2.h"

int main(void)
{
    Vec2 *left = Vec2(2.0f, 3.0f);
    Vec2 *right = Vec2();
    float rightward = Vec2_getRight(left);
    Vec2_setRight(left, 2.0f);
    float leftward = Vec2_getLeft(left);
    Vec2_setLeft(left, -2.0f);
    float upward = Vec2_getUp(left);
    Vec2_setUp(left, 3.0f);
    float downward = Vec2_getDown(left);
    Vec2_setDown(left, -3.0f);
    float x = Vec2_getX(left);
    Vec2_setX(left, 2.0f);
    float y = Vec2_getY(left);
    Vec2_setY(left, 3.0f);
    float frameY = Vec2_getYInFrame(left, COORD_FRAME_2D_Y_DOWN);
    Vec2_set(left, 2.0f, 3.0f);
    float dot = Vec2_dot(left, right);
    float lengthSquared = Vec2_lengthSquared(left);
    float length = Vec2_length(left);
    float distance = Vec2_distance(left, right);
    float angle = Vec2_angle(left, right);
    Vec2_free(right);
    Vec2_free(left);
    return 0;
}
```

## Vec2d class (vec2d.c)

`Vec2d_add`, `Vec2d_sub`, and `Vec2d_mul` still require caller-provided
destinations and are Value Return Law migration gaps. The scalar dot and length
results are shown as direct returns.

```c
#include "lang/vec2/vec2d.h"

int main(void)
{
    Vec2d *left = Vec2d(2.0, 3.0);
    Vec2d *right = Vec2d();
    double rightward = Vec2d_getRight(left);
    Vec2d_setRight(left, 2.0);
    double leftward = Vec2d_getLeft(left);
    Vec2d_setLeft(left, -2.0);
    double upward = Vec2d_getUp(left);
    Vec2d_setUp(left, 3.0);
    double downward = Vec2d_getDown(left);
    Vec2d_setDown(left, -3.0);
    double dot = Vec2d_dot(left, right);
    double length = Vec2d_length(left);
    Vec2d_free(right);
    Vec2d_free(left);
    return 0;
}
```

## Vec3d class (vec3d.c)

`Vec3d_add`, `Vec3d_sub`, `Vec3d_mul`, and `Vec3d_normalize` still require
caller-provided destinations and are Value Return Law migration gaps. The
scalar dot and length results are shown as direct returns.

```c
#include "lang/vec3/vec3d.h"

int main(void)
{
    Vec3d *left = Vec3d(1.0, 2.0, 3.0);
    Vec3d *right = Vec3d();
    double rightward = Vec3d_getRight(left);
    Vec3d_setRight(left, 1.0);
    double leftward = Vec3d_getLeft(left);
    Vec3d_setLeft(left, -1.0);
    double upward = Vec3d_getUp(left);
    Vec3d_setUp(left, 2.0);
    double downward = Vec3d_getDown(left);
    Vec3d_setDown(left, -2.0);
    double forward = Vec3d_getFront(left);
    Vec3d_setFront(left, 3.0);
    double backward = Vec3d_getBack(left);
    Vec3d_setBack(left, -3.0);
    double x = Vec3d_getX(left);
    double y = Vec3d_getY(left);
    double z = Vec3d_getZ(left);
    double dot = Vec3d_dot(left, right);
    double length = Vec3d_length(left);
    Vec3d_free(right);
    Vec3d_free(left);
    return 0;
}
```

## Vec3IntFloat class (vec3_int_float.c)

```c
#include "lang/vec3/vec3_int_float.h"

int main(void)
{
    Vec3IntFloat *position = Vec3IntFloat(9000, 1.0f, 0, 2.0f,
        -3000, 5.0f, COORD_FRAME_Y_UP_LEFT);
    Vec3IntFloat_rebalance(position, 1000.0f);
    float right = Vec3IntFloat_getRightLocal(position);
    float left = Vec3IntFloat_getLeftLocal(position);
    float up = Vec3IntFloat_getUpLocal(position);
    float down = Vec3IntFloat_getDownLocal(position);
    float front = Vec3IntFloat_getFrontLocal(position);
    float back = Vec3IntFloat_getBackLocal(position);
    Vec3IntFloat_free(position);
    return 0;
}
```

## Vec3LongDouble class (vec3_long_double.c)

```c
#include "lang/vec3/vec3_long_double.h"

int main(void)
{
    Vec3LongDouble *position = Vec3LongDouble(9000000, 1.0, 0, 2.0,
        -3000000, 5.0, COORD_FRAME_Y_UP_LEFT);
    Vec3LongDouble_rebalance(position, 1000000.0);
    double right = Vec3LongDouble_getRightLocal(position);
    double left = Vec3LongDouble_getLeftLocal(position);
    double up = Vec3LongDouble_getUpLocal(position);
    double down = Vec3LongDouble_getDownLocal(position);
    double front = Vec3LongDouble_getFrontLocal(position);
    double back = Vec3LongDouble_getBackLocal(position);
    Vec3LongDouble_free(position);
    return 0;
}
```

## Vec4 class (vec4.c)

`Vec4_copy`, `Vec4_add`, `Vec4_sub`, `Vec4_mul`, `Vec4_div`,
`Vec4_normalize`, and `Vec4_lerp` still require caller destinations and are
omitted under Value Return Law.

```c
#include "lang/vec4/vec4.h"

int main(void)
{
    Vec4 *left = Vec4();
    Vec4 *right = Vec4(1.0f, 2.0f, 3.0f, 1.0f);
    CoordFrame frame = COORD_FRAME_Y_UP_LEFT;
    float rightward = Vec4_getRight(left);
    Vec4_setRight(left, 1.0f);
    float leftward = Vec4_getLeft(left);
    Vec4_setLeft(left, -1.0f);
    float upward = Vec4_getUp(left);
    Vec4_setUp(left, 2.0f);
    float downward = Vec4_getDown(left);
    Vec4_setDown(left, -2.0f);
    float forward = Vec4_getFront(left);
    Vec4_setFront(left, 3.0f);
    float backward = Vec4_getBack(left);
    Vec4_setBack(left, -3.0f);
    float x = Vec4_getX(left);
    Vec4_setX(left, 1.0f);
    float y = Vec4_getY(left);
    Vec4_setY(left, 2.0f);
    float z = Vec4_getZ(left);
    Vec4_setZ(left, 3.0f);
    float w = Vec4_getW(left);
    Vec4_setW(left, 1.0f);
    float frameX = Vec4_getXInFrame(left, frame);
    float frameY = Vec4_getYInFrame(left, frame);
    float frameZ = Vec4_getZInFrame(left, frame);
    Vec4_set(left, 1.0f, 2.0f, 3.0f, 1.0f);
    float dot = Vec4_dot(left, right);
    float lengthSquared = Vec4_lengthSquared(left);
    float length = Vec4_length(left);
    Vec4_free(right);
    Vec4_free(left);
    return 0;
}
```

## Vec4d class (vec4d.c)

`Vec4d_add`, `Vec4d_sub`, and `Vec4d_mul` still require caller-provided
destinations and are Value Return Law migration gaps. The scalar dot and length
results are shown as direct returns.

```c
#include "lang/vec4/vec4d.h"

int main(void)
{
    Vec4d *left = Vec4d();
    Vec4d *right = Vec4d(1.0, 2.0, 3.0, 1.0);
    double rightward = Vec4d_getRight(left);
    Vec4d_setRight(left, 1.0);
    double leftward = Vec4d_getLeft(left);
    Vec4d_setLeft(left, -1.0);
    double upward = Vec4d_getUp(left);
    Vec4d_setUp(left, 2.0);
    double downward = Vec4d_getDown(left);
    Vec4d_setDown(left, -2.0);
    double forward = Vec4d_getFront(left);
    Vec4d_setFront(left, 3.0);
    double backward = Vec4d_getBack(left);
    Vec4d_setBack(left, -3.0);
    double dot = Vec4d_dot(left, right);
    double length = Vec4d_length(left);
    Vec4d_free(right);
    Vec4d_free(left);
    return 0;
}
```

## ImageMac class (image_mac.m)

`ImageMac_decode` returns pixels but requires caller-provided width and height
destinations. It is a migration gap under the value-return rule.

```c
int main(void)
{
    return 0;
}
```

## Dijkstra class (dijkstra.c)

`Dijkstra_shortestPath` writes the path and distance through caller-provided
destinations, so it is a migration gap under the value-return rule.

```c
#include "algo/dijkstra.h"

int main(void)
{
    DijkstraGraph *routes = Dijkstra(4u);
    bool addBiEdge = Dijkstra_addBiEdge(routes, 0u, 1u, 1.0f);
    bool addBiEdge2 = Dijkstra_addBiEdge(routes, 1u, 2u, 2.0f);
    bool addEdge = Dijkstra_addEdge(routes, 0u, 2u, 10.0f);
    Dijkstra_free(routes);
    return 0;
}
```

## Bvh class (bvh.c)

`BvhAabb_merge` and `BvhAabb_intersect_ray` write results through separate
destination arguments. The `BvhTree` operations that write a tree or hit through
an argument are also migration gaps under the value-return rule.

```c
#include "algo/bvh.h"

int main(void)
{
    float minimumPoint[3] = { -0.5f, -0.5f, -0.5f };
    float maximumPoint[3] = { 0.5f, 0.5f, 0.5f };
    float point[3] = { 0.0f, 0.0f, 0.0f };
    BvhAabb bounds = BvhAabb_empty();
    BvhAabb_setMinimum(&bounds, -0.5f, -0.5f, -0.5f);
    BvhAabb_setMaximum(&bounds, 0.5f, 0.5f, 0.5f);
    BvhAabb fromPoints = BvhAabb_from_points(minimumPoint, maximumPoint);
    BvhAabb_expand_point(point, &bounds);
    BvhRay ray = BvhRay(-2.0f, 0.0f, 0.0f, 1.0f, 0.0f,
        0.0f, 0.0f, 20.0f);
    BvhRay_setOrigin(&ray, -2.0f, 0.0f, 0.0f);
    BvhRay_setDirection(&ray, 1.0f, 0.0f, 0.0f);
    BvhRay_setRange(&ray, 0.0f, 20.0f);
    BvhPrimitive primitives[1];
    primitives[0] = BvhPrimitive(10u, bounds, 0.0f, 0.0f, 0.0f);
    BvhTree tree = BvhTree(1u);
    bool build = BvhTree_build(primitives, 1u, &tree);
    BvhRayHit hit = BvhRayHit();
    float nearDistance = 0.0f;
    bool boundsHit = BvhAabb_intersect_ray(&ray, &bounds, &nearDistance);
    bool treeHit = BvhTree_intersect_ray(&tree, &ray, &hit);
    BvhTree_destroy(&tree);
    return 0;
}
```

## Sort class (sort.c)

```c
#include "algo/sort.h"

int main(void)
{
    int32_t values[] = { 3, 1, 4, 2 };
    bool quickSort = Sort_quickSort(values, 4u, sizeof values[0], nullptr);
    bool insertionSort = Sort_insertionSort(values, 4u, sizeof values[0], nullptr);
    bool selectionSort = Sort_selectionSort(values, 4u, sizeof values[0], nullptr);
    bool bubbleSort = Sort_bubbleSort(values, 4u, sizeof values[0], nullptr);
    bool heapSort = Sort_heapSort(values, 4u, sizeof values[0], nullptr);
    int32_t scratch[4];
    bool mergeSort = Sort_mergeSort(values, 4u, sizeof values[0], nullptr, scratch);
    size_t partitionInt32 = Sort_partitionInt32(values, 4u, 3);
    uint32_t unsignedKeys[] = { 9u, 1u, 4u };
    uint64_t wideKeys[] = { 900u, 12u, 105u };
    uint64_t pairKeys[] = { 900u, 12u, 105u };
    int entities[] = { 90, 1, 10 };
    void *entityPointers[] = { &entities[0], &entities[1], &entities[2] };
    bool radixSortUint32 = Sort_radixSortUint32(unsignedKeys, 3u);
    bool radixSortUint64 = Sort_radixSortUint64(wideKeys, 3u);
    bool radixSortPairsUint64 = Sort_radixSortPairsUint64(pairKeys, entityPointers, 3u);
    return 0;
}
```

## Spatial class (spatial.c)

```c
#include "algo/spatial.h"

int main(void)
{
    uint64_t cellKey = Spatial_morton3D(12u, 4u, 9u);

    return 0;
}
```

## KdTree class (kd_tree.c)

`KdTree_nearest` and `KdTree_queryRadius` fill caller-provided result
destinations and are migration gaps under the value-return rule.

```c
#include "algo/kd_tree.h"

int main(void)
{
    KdPoint points[] = {
        KdPoint(1.0f, 2.0f, 0.0f, 101u),
        KdPoint(5.0f, 2.0f, 0.0f, 202u)
    };
    KdTree *tree = KdTree_build(points, 2u);
    KdTree_free(tree);
    return 0;
}
```

## SegmentIndex class (segment_index.c)

`SegmentIndex_segment`, `SegmentIndex_query`, and both string projections fill
caller-owned destinations. `SegmentIndex_toString` and
`SegmentIndex_toStringStruct` are the projection migration gaps. The legacy
`SegmentIndex_init` initializer also has no constructor-macro call form; that
constructor lifecycle remains a separate gap.

```c
#include "algo/segment_index.h"

int main(void)
{
    const char *propertyPath = "character.position.horizontal";
    uint32_t pathSegmentCount = SegmentIndex_segmentCount(propertyPath);
    SegmentIndex *index = SegmentIndex();
    SegmentIndex_clear(index);
    uint32_t add = SegmentIndex_add(index, propertyPath, 501u);
    size_t buildFrom = SegmentIndex_buildFrom(index, nullptr);
    size_t buildFromMini = SegmentIndex_buildFromMini(index, nullptr);
    uint32_t segmentCount = SegmentIndex_count(index);
    bool isEmpty = SegmentIndex_isEmpty(index);
    SegmentIndex_shutdown(index);
    SegmentIndex_free(index);
    return 0;
}
```

## TreeSitTree class (tree_sit.c)

`TreeSitTree_walk_preorder` and `TreeSitTree_walk_postorder` require a visitor
callback, which this one-main-only example cannot define; both remain callback
API gaps.

```c
#include "algo/tree_sit.h"

int main(void)
{
    TreeSitTree tree = TreeSitTree(8u);
    TreeSitSpan file = TreeSitSpan(0u, 12u, 0u, 0u, 0u, 12u);
    TreeSitSpan word = TreeSitSpan(4u, 8u, 0u, 4u, 0u, 8u);
    int32_t root = TreeSitTree_add_node(-1, 1u, "file", file, &tree);
    int32_t node = TreeSitTree_add_node(root, 2u, "name", word, &tree);
    int32_t foundNode = TreeSitTree_find_by_byte(&tree, 5u);
    uint32_t matchingNodeCount = TreeSitTree_count_kind(&tree, 2u);
    TreeSitTree_destroy(&tree);
    return 0;
}
```

## RingBuffer class (ring.c)

`RingBuffer_pop` fills a caller-provided value destination and remains a
migration gap under the value-return rule.

```c
#include "atomic/ring.h"

int main(void)
{
    RingBuffer queue = RingBuffer(sizeof(uint32_t), 4u);
    uint32_t submitted = 73u;
    bool push = RingBuffer_push(&queue, &submitted);
    RingBuffer_shutdown(&queue);
    return 0;
}
```

## ThreadRegistry class (registry.c)

```c
#include "atomic/registry.h"

int main(void)
{
    int workerIndex = ThreadRegistry_index();
    ThreadRegistry_setRole(workerIndex, THREAD_ROLE_USER);
    int role = ThreadRegistry_role(workerIndex);
    const char *roleName = ThreadRegistry_roleName(THREAD_ROLE_USER);
    return 0;
}
```

## SpinLock class (spin.c)

```c
#include "atomic/spin.h"

int main(void)
{
    SpinLock lock = SPIN_LOCK_INIT;
    SpinLock_lock(&lock);
    bool tryAcquired = SpinLock_tryLock(&lock);
    bool acquired = SpinLock_tryLockTimeout(&lock, 1000000);
    SpinLock_unlock(&lock);
    bool locked = SpinLock_isLocked(&lock);



    return 0;
}
```

## BitPool class (bit.c)

```c
#include "bit/bit.h"
#include "oop/type.h"

int main(void)
{
    BitPool pool = BitPool(sizeof(uint32_t), 8u);
    uint32_t *slot = BitPool_alloc(&pool, TYPE_INT_SINGLETON);
    bool containsSlot = BitPool_contains(&pool, slot);
    uint64_t slotType = BitPool_type(&pool, slot);
    size_t slotLength = BitPool_length(&pool, slot);
    BitPool_free(&pool, slot);
    BitPool_shutdown(&pool);
    return 0;
}
```

## Function class (fn.h)

`Function_setCall`, `Function_run`, and `Function_bind` need a real callback,
which this one-main example cannot define; those calls remain callback gaps.

```c
#include "c23/fn.h"

int main(void)
{
    Function function = Function();
    int functionContext = 73;
    bool contextSet = Function_setContext(&function, &functionContext);
    FunctionCallFn call = Function_getCall(&function);
    void *context = Function_getContext(&function);
    return 0;
}
```

## TryCode class (try_code.c)

```c
#include "exception/try_code.h"

int main(void)
{
    const char *name = TryCode_name(TRY_NOT_FOUND);
    const char *message = TryCode_message(TRY_NOT_FOUND);
    bool isOk = TryCode_isOk(TRY_OK);
    return 0;
}
```

## Console class (console.c)

This process-wide API has no `Console(...)` constructor macro. `Console_init()`
is a compatibility no-op, so it is not shown as construction.

```c
#include "cli/console.h"
#include "primitive/string.h"

int main(void)
{
    Console_log("import complete");
    uint8_t *message = String("owned message goes here");
    Console_logString(message);
    Console_drain();
    Console_shutdown();
    return 0;
}
```

## Dispatch class (dispatch.c)

`Dispatch_post` requires a callback definition, which the one-main-only format
cannot provide; posting remains a callback API gap.

```c
#include "deferred/dispatch.h"

int main(void)
{
    Dispatch *dispatch = Dispatch();
    bool drain = Dispatch_drain(dispatch);
    size_t pending = Dispatch_pending(dispatch);
    uint64_t drainedCount = Dispatch_getDrainedCount(dispatch);
    bool isFreed = Dispatch_free(dispatch);
    return 0;
}
```

## Focus class (focus.c)

```c
#include "input/focus.h"

int main(void)
{
    Focus_set(17u);
    bool isFocused = Focus_isFocused(17u);
    uint32_t focusedWindowId = Focus_id();
    Focus_set(FOCUS_BROADCAST);
    return 0;
}
```

## Key class (key.c)

This process-wide subsystem has no `Key(...)` constructor macro. `Key_init()`
is a legacy bootstrap call and is omitted; event producers initialize lazily.
`Key_addListener`, `Key_removeListener`, `Key_attachWindow`, and
`Key_detachWindow` need a real `KeyHandler`; the handler has callback fields
but no constructor or setters, so those calls are gaps in this one-main example.

```c
#include "input/key.h"

int main(void)
{
    Key_detachWindowAll(7u);
    Key_pushEvent(7u, KEY_A, KEY_ACTION_DOWN, 250000000u);
    Key_pushCharEvent(7u, 'a');
    Key_dispatchEvents();
    bool isDown = Key_isDown(KEY_A);
    uint64_t pressTime = Key_pressTime(KEY_A);
    uint64_t lastReleaseTime = Key_lastReleaseTime(KEY_A);
    uint64_t lastHoldDuration = Key_lastHoldDurationNanos(KEY_A);
    uint64_t currentHoldDuration = Key_currentHoldDurationNanos(KEY_A);
    uint64_t holdDuration = Key_holdDurationNanos(KEY_A);
    uint64_t durationSinceRelease = Key_durationSinceReleaseNanos(KEY_A);
    int tapCount = Key_taps(KEY_A);
    Key_resetTaps(KEY_A);
    KeyTapPhase tapPhase = Key_tapPhase(KEY_A);
    bool longPressFired = Key_isLongPressFired(KEY_A);
    Key_setLongPressFired(KEY_A, false);
    int keyCode = Key_code(KEY_A);
    bool hasShift = Key_hasShift(KEY_A);
    bool hasControl = Key_hasControl(KEY_A);
    bool hasOption = Key_hasOption(KEY_A);
    bool hasCommand = Key_hasCommand(KEY_A);
    const char *keyName = Key_name(KEY_A);
    Key_shutdown();
    return 0;
}
```

## Gamepad class (gamepad.c)

`GamepadState` exposes its button setter, but does not yet expose setters or
getters for the stick, trigger, rumble, or connection fields.

```c
#include "input/gamepad.h"

int main(void)
{
    GamepadState gamepad = GamepadState();
    GamepadState_setButtons(&gamepad, GAMEPAD_BUTTON_A | GAMEPAD_BUTTON_START);
    bool buttonDown = GamepadState_isDown(&gamepad, GAMEPAD_BUTTON_A);
    Vec2 rawStick;
    Vec2_set(&rawStick, 0.8f, 0.0f);
    Vec2 filteredStick = Gamepad_applyCircularDeadzone(rawStick, GAMEPAD_DEFAULT_DEADZONE);

    return 0;
}
```

## Turntable class (turntable.c)

```c
#include "input/turntable.h"

int main(void)
{
    TurntableEvent event = TurntableEvent(0u, true, 0.5f);
    TurntableEvent_setPlatterTouched(&event, true);
    TurntableEvent_setAngularDelta(&event, 0.5f);
    TurntableState turntable = TurntableState(0u);
    TurntableState_processEvent(&turntable, event);
    TurntableState_tick(&turntable, 0.016f);
    TurntableCrossfade volumes = Turntable_calculateCrossfade(0.0f, CROSSFADER_LINEAR);

    return 0;
}
```

## Mouse class (mouse.c)

This process-wide subsystem has no `Mouse(...)` constructor macro. `Mouse_init()`
is a legacy bootstrap call and is omitted; event producers initialize lazily.
`Mouse_addListener`, `Mouse_removeListener`, `Mouse_attachWindow`, and
`Mouse_detachWindow` need a real `MouseHandler`; the handler has callback fields
but no constructor or setters, so those calls are gaps in this one-main example.

```c
#include "input/mouse.h"
#include "input/key.h"

int main(void)
{
    Mouse_detachWindowAll(7u);
    Mouse_pushButtonEvent(7u, MOUSE_LEFT, KEY_ACTION_DOWN, 250000000u);
    Mouse_pushMoveEvent(7u, 14.0, 29.0);
    Mouse_pushMoveDeltaEvent(7u, 1.0, 2.0);
    Mouse_pushDragEvent(7u, MOUSE_LEFT, 14.0, 29.0);
    Mouse_pushScrollEvent(7u, 1.0, 2.0);
    Mouse_pushZoomEvent(7u, 0.25);
    Mouse_dispatchEvents();
    bool isDown = Mouse_isDown(MOUSE_LEFT);
    uint64_t pressTime = Mouse_pressTime(MOUSE_LEFT);
    uint64_t lastReleaseTime = Mouse_lastReleaseTime(MOUSE_LEFT);
    uint64_t lastHoldDuration = Mouse_lastHoldDurationNanos(MOUSE_LEFT);
    uint64_t currentHoldDuration = Mouse_currentHoldDurationNanos(MOUSE_LEFT);
    int tapCount = Mouse_taps(MOUSE_LEFT);
    Mouse_resetTaps(MOUSE_LEFT);
    MouseTapPhase tapPhase = Mouse_tapPhase(MOUSE_LEFT);
    bool longPressFired = Mouse_isLongPressFired(MOUSE_LEFT);
    Mouse_setLongPressFired(MOUSE_LEFT, false);
    double x = Mouse_x();
    double y = Mouse_y();
    int button = Mouse_button(MOUSE_LEFT);
    bool hasShift = Mouse_hasShift(MOUSE_LEFT);
    bool hasControl = Mouse_hasControl(MOUSE_LEFT);
    bool hasOption = Mouse_hasOption(MOUSE_LEFT);
    bool hasCommand = Mouse_hasCommand(MOUSE_LEFT);
    const char *buttonName = Mouse_name(MOUSE_LEFT);
    Mouse_shutdown();
    return 0;
}
```

## Touch class (touch.c)

This process-wide subsystem has no `Touch(...)` constructor macro. `Touch_init()`
is a legacy bootstrap call and is omitted; event producers initialize lazily.
`Touch_addListener`, `Touch_removeListener`, `Touch_attachWindow`, and
`Touch_detachWindow` need a real `TouchHandler`; the handler has callback fields
but no constructor or setters, so those calls are gaps in this one-main example.

```c
#include "input/touch.h"

int main(void)
{
    Touch_detachWindowAll(7u);
    Touch_pushTouchEvent(7u, 2, TOUCH_DOWN, 10.0, 20.0, 0.5, 250000000u);
    Touch_dispatchEvents();
    bool isDown = Touch_isDown(2);
    uint64_t pressTime = Touch_pressTime(2);
    uint64_t lastHoldDuration = Touch_lastHoldDuration(2);
    int tapCount = Touch_taps(2);
    int lastAction = Touch_lastAction(2);
    double x = Touch_x(2);
    double y = Touch_y(2);
    double pressure = Touch_pressure(2);
    Touch_shutdown();
    return 0;
}
```

## KeyMap class (key_map.c)

`KeyMap_resolve` writes the resolved combo through a caller-provided pointer.
`KeyMap_bind` and `KeyMap_unbind` require a real `KeyBindingFn`, which this
one-main example cannot define; these remain explicit API gaps.

```c
#include "input/key_map.h"
#include "input/key.h"
#include "input/mouse.h"

int main(void)
{
    KeyMap *bindings = KeyMap(nullptr);
    int64_t combo = KeyMap_buildCombo(KEY_A, KMODE_TAP);
    int64_t buildComboForKey = KeyMap_buildComboForKey(KEY_A, KMODE_TAP);
    int64_t buildComboForMouse = KeyMap_buildComboForMouse(MOUSE_LEFT, KMODE_TAP);
    int64_t buildComboForHold = KeyMap_buildComboForHold(KEY_A, KEYMAP_LONG_PRESS_NANOS);
    const KeyBinding *binding = KeyMap_match(bindings, combo);
    bool multiTapEnabled = KeyMap_isMultiTapEnabled(bindings);
    KeyMap_setMultiTapEnabled(bindings, true);
    uint64_t longPressNanos = KeyMap_getLongPressNanos(bindings);
    KeyMap_setLongPressNanos(bindings, KEYMAP_LONG_PRESS_NANOS);
    uint32_t bindingCount = KeyMap_count(bindings);
    bool isEmpty = KeyMap_isEmpty(bindings);
    KeyMap_destroy(bindings);
    return 0;
}
```

## CoordFrame class (coord_frame.c)

```c
#include "math/coord_frame.h"

int main(void)
{
    CoordBasis basis = CoordFrame_getBasis(COORD_FRAME_Y_UP_LEFT);
    int axisIndex = CoordFrame_getAxisIndex(COORD_FRAME_Y_UP_LEFT, 0);
    int axisSign = CoordFrame_getAxisSign(COORD_FRAME_Y_UP_LEFT, 0);
    bool isValid = CoordFrame_isValid(COORD_FRAME_Y_UP_LEFT);
    const char *name = CoordFrame_name(COORD_FRAME_Y_UP_LEFT);
    return 0;
}
```

## StrictMath class (strict_math.c)

```c
#include "math/strict_math.h"

int main(void)
{
    float sine = StrictMath_sin(0.5f);
    float cosine = StrictMath_cos(0.5f);
    float tangent = StrictMath_tan(0.5f);
    float arcSine = StrictMath_asin(0.5f);
    float arcCosine = StrictMath_acos(0.5f);
    float arcTangent = StrictMath_atan(0.5f);
    float arcTangent2 = StrictMath_atan2(0.5f, 1.0f);
    float root = StrictMath_sqrt(4.0f);
    float inverseRoot = StrictMath_invSqrt(4.0f);
    float power = StrictMath_pow(2.0f, 3.0f);
    float exponential = StrictMath_exp(1.0f);
    float logarithm = StrictMath_log(2.0f);
    float absolute = StrictMath_abs(-1.0f);
    float floorValue = StrictMath_floor(1.5f);
    float ceiling = StrictMath_ceil(1.5f);
    float rounded = StrictMath_round(1.5f);
    float clamped = StrictMath_clamp(2.0f, 0.0f, 1.0f);
    float interpolated = StrictMath_lerp(0.0f, 1.0f, 0.5f);
    float radians = StrictMath_toRadians(90.0f);
    float degrees = StrictMath_toDegrees(1.0f);
    double sineD = StrictMath_sinD(0.5);
    double cosineD = StrictMath_cosD(0.5);
    double tangentD = StrictMath_tanD(0.5);
    double arcSineD = StrictMath_asinD(0.5);
    double arcCosineD = StrictMath_acosD(0.5);
    double arcTangentD = StrictMath_atanD(0.5);
    double arcTangent2D = StrictMath_atan2D(0.5, 1.0);
    double rootD = StrictMath_sqrtD(4.0);
    double inverseRootD = StrictMath_invSqrtD(4.0);
    double powerD = StrictMath_powD(2.0, 3.0);
    double exponentialD = StrictMath_expD(1.0);
    double logarithmD = StrictMath_logD(2.0);
    double absoluteD = StrictMath_absD(-1.0);
    double floorValueD = StrictMath_floorD(1.5);
    double ceilingD = StrictMath_ceilD(1.5);
    double roundedD = StrictMath_roundD(1.5);
    double clampedD = StrictMath_clampD(2.0, 0.0, 1.0);
    double interpolatedD = StrictMath_lerpD(0.0, 1.0, 0.5);

    return 0;
}
```

## FastMath class (fast_math.c)

```c
#include "math/fast_math.h"

int main(void)
{
    float inverseRoot = FastMath_invSqrt(4.0f);
    float inverse = FastMath_inv(4.0f);
    float sine = FastMath_sin(0.5f);
    float cosine = FastMath_cos(0.5f);
    float tangent = FastMath_tan(0.5f);
    float arcTangent = FastMath_atan(0.5f);
    float arcTangent2 = FastMath_atan2(0.5f, 1.0f);
    float absolute = FastMath_abs(-1.0f);
    float rounded = FastMath_round(1.5f);
    float clamped = FastMath_clamp(2.0f, 0.0f, 1.0f);
    float interpolated = FastMath_lerp(0.0f, 1.0f, 0.5f);
    bool approximatelyEqual = FastMath_approxEqual(1.0f, 1.0f, 0.001f);
    float radians = FastMath_toRadians(90.0f);
    float degrees = FastMath_toDegrees(1.0f);
    return 0;
}
```

## Math class (math.c)

```c
#include "math/math.h"

int main(void)
{
    float sine = Math_sin(0.5f);
    float cosine = Math_cos(0.5f);
    float tangent = Math_tan(0.5f);
    float arcSine = Math_asin(0.5f);
    float arcCosine = Math_acos(0.5f);
    float arcTangent = Math_atan(0.5f);
    float arcTangent2 = Math_atan2(0.5f, 1.0f);
    float root = Math_sqrt(4.0f);
    float inverseRoot = Math_invSqrt(4.0f);
    float power = Math_pow(2.0f, 3.0f);
    float exponential = Math_exp(1.0f);
    float logarithm = Math_log(2.0f);
    float absolute = Math_abs(-1.0f);
    float floorValue = Math_floor(1.5f);
    float ceiling = Math_ceil(1.5f);
    float rounded = Math_round(1.5f);
    float clamped = Math_clamp(2.0f, 0.0f, 1.0f);
    float interpolated = Math_lerp(0.0f, 1.0f, 0.5f);
    float radians = Math_toRadians(90.0f);
    float degrees = Math_toDegrees(1.0f);
    double sineD = Math_sinD(0.5);
    double cosineD = Math_cosD(0.5);
    double rootD = Math_sqrtD(4.0);
    double arcTangent2D = Math_atan2D(0.5, 1.0);
    float fastSine = Math_fast_sin(0.5f);
    float fastCosine = Math_fast_cos(0.5f);
    float fastTangent = Math_fast_tan(0.5f);
    float fastArcTangent = Math_fast_atan(0.5f);
    float fastArcTangent2 = Math_fast_atan2(0.5f, 1.0f);
    float fastInverseRoot = Math_fast_invSqrt(4.0f);
    float fastInverse = Math_fast_inv(2.0f);
    float fastAbsolute = Math_fast_abs(-1.0f);
    float fastRounded = Math_fast_round(1.5f);
    float fastClamped = Math_fast_clamp(2.0f, 0.0f, 1.0f);
    float fastInterpolated = Math_fast_lerp(0.0f, 1.0f, 0.5f);
    bool fastApproximatelyEqual = Math_fast_approxEqual(1.0f, 1.0f, 0.001f);
    return 0;
}
```

## Calc class (calc.c)

`Calc_eval` and `Calc_evalFloat` write numeric results through caller-provided
destinations. `Calc_evalWithFallback` returns its result directly and remains
the call shown here.

```c
#include "search/calc.h"

int main(void)
{
    double result = Calc_evalWithFallback("2 + 3 * 4", 0.0);

    return 0;
}
```

## Search class (find.c)

```c
#include "search/find.h"

int main(void)
{
    bool hasExactMatch = Search_match("player health", "health", FIND_EXACT_WORD);
    int32_t firstMatch = Search_findFirst("player health", "health", FIND_DEFAULT);
    bool matchesPattern = Search_like("value", "val%", false);
    bool hasWholeWord = Search_exactWord("player health", "health", false);
    return 0;
}
```

## Spotlight class (spotlight.c)

`Spotlight_rank` fills a caller-provided match array, and
`Spotlight_tryCalculate` fills a caller-provided numeric-result pointer. Both
are migration gaps under the value-return rule.

```c
int main(void)
{
    return 0;
}
```

## Calendar class (calendar.c)

```c
#include "time/calendar.h"

int main(void)
{
    DateTime date = DateTime();
    bool isLeapYear = Calendar_isLeapYear(2024);
    int32_t daysInMonth = Calendar_daysInMonth(2024, 2);
    int32_t weekday = Calendar_dayOfWeek(2024, 2, 29);
    Calendar_addDays(&date, 1);
    Calendar_addMonths(&date, 1);
    Calendar_addYears(&date, 1);
    return 0;
}
```

## DateTime class (datetime.c)

```c
#include "time/datetime.h"

int main(void)
{
    DateTime date = DateTime();
    DateTime_set(&date);
    setEpochMillis(&date, 1792056600000LL);
    int64_t epochMillis = DateTime_epochMillis(&date);
    int32_t year = DateTime_year(&date);
    int32_t month = DateTime_month(&date);
    int32_t day = DateTime_day(&date);
    int32_t hour = DateTime_hour(&date);
    int32_t minute = DateTime_minute(&date);
    int32_t second = DateTime_second(&date);
    int32_t millisecond = DateTime_millisecond(&date);
    int32_t weekday = DateTime_dayOfWeek(&date);
    return 0;
}
```

## Clock class (clock.c)

```c
#include "time/clock.h"

int main(void)
{
    Clock clock = Clock();
    Clock_tick(&clock);
    Clock_setTimeScale(&clock, 0.5);
    double timeScale = Clock_timeScale(&clock);
    Clock_setPaused(&clock, true);
    bool isPaused = Clock_isPaused(&clock);
    uint64_t virtualTimeMillis = Clock_virtualTimeMillis(&clock);
    Clock_reset(&clock);
    return 0;
}
```

## NanoTime and NanoTimer classes (nanotime.c)

The process clock has no `NanoTime(...)` constructor macro, and `NanoTimer` has
no `NanoTimer(...)` constructor macro. The `NanoTime_init()` and
`NanoTimer_reset()` lifecycle calls are not shown as constructors, so only the
raw monotonic reading is directly usable in this example.
`NanoTime_startNanos` and `NanoTime_elapsedNanos` require the process bootstrap;
`NanoTimer_tick`, `NanoTimer_tickWithClock`, `NanoTimer_deltaTime`,
`NanoTimer_totalTime`, `NanoTimer_deltaNanos`, and
`NanoTimer_elapsedNanosOf` require a constructed timer value.

```c
#include "time/nanotime.h"

int main(void)
{
    uint64_t nowNanos = NanoTime_now();
    return 0;
}
```

## Arrays class (arrays.c)

`Arrays_copy` currently accepts a caller-provided destination buffer. That
legacy signature must be migrated before this example can follow the Value
Return Law.

```c
#include "util/arrays.h"

int main(void)
{
    int32_t intValues[] = { 3, 1, 2 };
    int64_t longValues[] = { 3, 1, 2 };
    uint8_t sourceBytes[] = { 1u, 2u, 3u };
    Arrays_sortInt(intValues, 3u);
    Arrays_sortLong(longValues, 3u);
    intptr_t intIndex = Arrays_binarySearchInt(intValues, 3u, 2);
    intptr_t longIndex = Arrays_binarySearchLong(longValues, 3u, 2);
    Arrays_fill(sourceBytes, sizeof sourceBytes, 0u);
    /* Arrays_copy is omitted: its API takes a separate destination buffer. */
    return 0;
}
```

## Hash class (hash.c)

```c
#include "util/hash.h"

int main(void)
{
    const uint8_t data[] = "hash-input-goes-here";
    uint64_t contentHash = Hash_fnv1a64(data, sizeof data);
    uint64_t pointerHash = Hash_pointer(data);
    uint64_t mixed64 = Hash_murmur3Mix64(42u);
    uint32_t mixed32 = Hash_murmur3Mix32(42u);
    return 0;
}
```

## Url class (url.c)

`Url_build`, `Url_base64`, `Url_basicAuth`, and `Url_bearerAuth` still write
into caller-provided output buffers. Those signatures must be migrated before
they can be called under the Value Return Law. `Url_defaultPort` returns its
value directly.

```c
#include "net/url.h"

int main(void)
{
    const uint8_t inputBytes[] = "value-to-encode";
    int defaultPort = Url_defaultPort("https");

    return 0;
}
```

## Json class (json.c)

`Json_parse` needs caller-owned node and scratch storage, while `JsonWriter(...)`
and `Json_writeNumber`, `Json_writeString`, and `Json_writeBool` need caller-owned
output buffers. `JsonWriter_ok`, `JsonWriter_used`, `Json_beginObject`,
`Json_endObject`, `Json_beginArray`, `Json_endArray`, `Json_addKey`,
`Json_stringVal`, `Json_numberVal`, `Json_boolVal`, `Json_nullVal`, and
`Json_rawVal` all require that writer. `Json_string` and `Json_key` also use
caller-provided length outputs. Without destination-free constructors, the
navigation APIs (`Json_root`, `Json_ok`, `Json_member`, `Json_at`, `Json_count`,
`Json_type`, `Json_bool`, `Json_number`, `Json_has`, `Json_path`, `Json_getBool`,
`Json_getNumber`, and `Json_getString`) cannot be demonstrated on a constructed
document. These remain value-return and constructor gaps.

```c
int main(void)
{
    return 0;
}
```

## Net class (netfacade.c)

`Net_get`, `Net_getJson`, and `Net_postJson` write response content or parsed
JSON state into caller-owned buffers and records. They are migration gaps under
the value-return rule, so no destination-based calls are shown.

```c
int main(void)
{
    return 0;
}
```

## Http class (http.c)

`Http_perform` fills a caller-provided response buffer, and
`HttpServer_start` writes the bound port through an output pointer.
`HttpServer_stop` needs an initialized `HttpServer`, but neither `HttpServer`
nor `HttpHeader` has a preferred constructor macro. `Http_respond` also needs a
live descriptor supplied by a running handler. These APIs are migration gaps.

```c
#include "net/http.h"

int main(void)
{
    HttpRequest request = HttpRequest("api.example.test", 80, "/status");
    HttpRequest_setScheme(&request, "http");
    HttpRequest_setMethod(&request, "GET");
    HttpRequest_setHeaders(&request, nullptr, 0u);
    HttpRequest_setBody(&request, "{}", 2u);
    HttpRequest_setTimeout(&request, 5000u);
    return 0;
}
```

## Download class (download.c)

`Download_to_memory` writes through a response pointer, and
`Download_fetch_cached` fills a caller-owned path buffer. They are migration
gaps; file download keeps its path argument as the intended file destination.

```c
#include "net/download.h"

int main(void)
{
    DownloadOptions options = DownloadOptions();
    DownloadOptions_setTimeout(&options, 30u);
    DownloadOptions_setFollowRedirects(&options, true);
    DownloadOptions_setSilent(&options, true);
    DownloadOptions_setUserAgent(&options, "client-name-goes-here/1.0");
    bool downloaded = Download_to_file("https://example.test/archive", "download-path-goes-here",
        &options);
    DownloadResponse response = DownloadResponse();
    DownloadResponse_free(&response);
    return 0;
}
```

## Apple TLS backend (net/tls_apple.m)

The backend does not provide a `TlsConn(...)` constructor macro. `Tls_connect`
returns its handle through an output pointer, and `Tls_recv` writes into a
caller-provided buffer and count. `Tls_send`, `Tls_readable`, `Tls_setBudget`,
`Tls_getBudget`, and `Tls_close` need a live connection from that unavailable
constructor path. These operations remain constructor/value-return gaps; the
backend selector returns directly and is shown below.

```c
#include "net/tls.h"

int main(void)
{
    TlsBackendKind backend = Tls_backend();
    return 0;
}
```

## Curl TLS backend (net/tls_curl.c)

The curl backend has the same seam and the same missing `TlsConn(...)`
constructor macro. `Tls_connect` returns its handle through an output pointer,
and `Tls_recv` writes into a caller-provided buffer and count. `Tls_send`,
`Tls_readable`, `Tls_setBudget`, `Tls_getBudget`, and `Tls_close` need a live
connection from that unavailable constructor path. These operations remain
constructor/value-return gaps; the backend selector returns directly and is
shown below.

```c
#include "net/tls.h"

int main(void)
{
    TlsBackendKind backend = Tls_backend();
    return 0;
}
```

## Audio, AudioClip, and AudioVoice classes (audio_stub.c)

This file is the silent backend: `Audio_init()` returns `false`, constructors
return null handles, and playback is a no-op. `AudioClip` has no
`AudioClip(...)` constructor macro, so its factory, duration, and free functions
are shown as direct API calls and remain preferred-constructor gaps. The
shared `Audio_init`/`Audio_shutdown` lifecycle calls are also shown directly.

```c
#include "audio/audio.h"

int main(void)
{
    bool initialized = Audio_init();
    bool audioReady = Audio_isReady();
    AudioVoice *voice = AudioVoice();
    AudioClip *loadedClip = AudioClip_load("audio-file-path-goes-here");
    AudioClip *toneClip = AudioClip_tone(440.0f, 1.0f);
    float loadedDuration = AudioClip_seconds(loadedClip);
    float toneDuration = AudioClip_seconds(toneClip);
    AudioVoice_setClip(voice, nullptr);
    AudioVoice_setGain(voice, 0.75f);
    AudioVoice_setPitch(voice, 1.0f);
    AudioVoice_setLooping(voice, true);
    AudioVoice_play(voice);
    AudioVoice_pause(voice);
    AudioVoice_stop(voice);
    bool voiceIsPlaying = AudioVoice_isPlaying(voice);
    AudioVoice *nullVoice = AudioVoice();
    AudioVoice_free(nullVoice);
    Audio *silent = Audio();
    Audio *fromFile = Audio("audio-file-path-goes-here");
    Audio *customRate = Audio(48000.0);
    Audio *customChannels = Audio(48000.0, AUDIO_MONO);
    Audio_play(silent);
    Audio_pause(silent);
    Audio_stop(silent);
    bool isPlaying = Audio_isPlaying(silent);
    Audio_setGain(silent, 0.75f);
    float gain = Audio_getGain(silent);
    Audio_setPitch(silent, 1.0f);
    float pitch = Audio_getPitch(silent);
    Audio_setLooping(silent, true);
    bool looping = Audio_getLooping(silent);
    Audio_setSampleRate(silent, 48000.0);
    double sampleRate = Audio_getSampleRate(silent);
    Audio_setChannels(silent, AUDIO_STEREO);
    int channels = Audio_getChannels(silent);
    Audio *fromRate = Audio(48000.0);
    Audio *fromRateAndChannels = Audio(48000.0, AUDIO_MONO);
    Audio_free(fromRateAndChannels);
    Audio_free(fromRate);
    AudioVoice_free(voice);
    AudioClip_free(toneClip);
    AudioClip_free(loadedClip);
    Audio_free(customChannels);
    Audio_free(customRate);
    Audio_free(fromFile);
    Audio_free(silent);
    Audio_shutdown();
    return 0;
}
```

## AudioHal class (audio_hal_stub.c)

```c
#include "audio/audio_hal.h"

int main(void)
{
    AudioHalConfig config = AudioHalConfig();
    bool sampleRateSet = AudioHalConfig_set_sample_rate(&config, 48000.0);
    bool channels = AudioHalConfig_set_channels(&config, 2u);
    bool frames = AudioHalConfig_set_buffer_frames(&config, 256u);
    AudioHal *hal = AudioHal(&config);
    bool isStarted = AudioHal_start(hal);
    bool isRunning = AudioHal_is_running(hal);
    double sampleRate = AudioHal_get_sample_rate(hal);
    uint32_t channelCount = AudioHal_get_channels(hal);
    uint32_t bufferFrames = AudioHal_get_buffer_frames(hal);
    double latencyMs = AudioHal_get_latency_ms(hal);
    bool stop = AudioHal_stop(hal);
    AudioHal_destroy(hal);
    return 0;
}
```

## Bool class (bool.c)

`Bool_alloc`, `Bool_allocArray`, and `Bool_allocWithValue` are the low-level
allocation functions behind `Bool(...)` and `Bool_array(...)`; examples use
those preferred macro forms. `Bool_init` and `Bool_shutdown` manage the backing
pool lifecycle, but
`_init()` calls are excluded from cookbook examples. Pool bootstrap and teardown
remain lifecycle gaps; `Bool(...)` is the value constructor.

```c
#include "primitive/bool.h"

int main(void)
{
    void *enabled = Bool(true);
    void *enabledValues = Bool_array(4u);
    bool enabledValue = Bool_get(enabled);
    Bool_set(enabled, false);
    bool compareAndSet = Bool_compareAndSet(enabled, false, true);
    uint64_t enabledType = Bool_type(enabled);
    size_t enabledLength = Bool_length(enabled);
    Bool_free(enabledValues);
    Bool_free(enabled);
    return 0;
}
```

## Byte class (byte.c)

`Byte_alloc`, `Byte_allocArray`, and `Byte_allocWithValue` are the low-level
allocation functions behind `Byte(...)` and `Byte_array(...)`; examples use
those preferred macro forms. `Byte_init` and `Byte_shutdown` manage the backing
pool lifecycle, but
`_init()` calls are excluded from cookbook examples. Pool bootstrap and teardown
remain lifecycle gaps; `Byte(...)` is the value constructor.

```c
#include "primitive/byte.h"

int main(void)
{
    void *value = Byte(7);
    void *values = Byte_array(4u);
    int8_t byteValue = Byte_get(value);
    Byte_set(value, 8);
    bool compareAndSet = Byte_compareAndSet(value, 8, 9);
    uint64_t valueType = Byte_type(value);
    size_t valueLength = Byte_length(value);
    Byte_free(values);
    Byte_free(value);
    return 0;
}
```

## Short class (short.c)

`Short_alloc`, `Short_allocArray`, and `Short_allocWithValue` are the low-level
allocation functions behind `Short(...)` and `Short_array(...)`; examples use
those preferred macro forms. `Short_init` and `Short_shutdown` manage the
backing pool lifecycle, but
`_init()` calls are excluded from cookbook examples. Pool bootstrap and teardown
remain lifecycle gaps; `Short(...)` is the value constructor.

```c
#include "primitive/short.h"

int main(void)
{
    void *value = Short(300);
    void *values = Short_array(4u);
    int16_t shortValue = Short_get(value);
    Short_set(value, 301);
    bool compareAndSet = Short_compareAndSet(value, 301, 302);
    uint64_t valueType = Short_type(value);
    size_t valueLength = Short_length(value);
    Short_free(values);
    Short_free(value);
    return 0;
}
```

## Int class (int.c)

`Int_alloc`, `Int_allocArray`, and `Int_allocWithValue` are the low-level
allocation functions behind `Int(...)` and `Int_array(...)`; examples use those
preferred macro forms. `Int_init` and `Int_shutdown` manage the backing pool
lifecycle, but `_init()`
calls are excluded from cookbook examples. Pool bootstrap and teardown remain
lifecycle gaps; `Int(...)` is the value constructor.

```c
#include "primitive/int.h"

int main(void)
{
    void *value = Int(42000);
    void *values = Int_array(4u);
    int32_t integerValue = Int_get(value);
    Int_set(value, 42);
    bool compareAndSet = Int_compareAndSet(value, 42, 43);
    uint64_t valueType = Int_type(value);
    size_t valueLength = Int_length(value);
    Int_free(values);
    Int_free(value);
    return 0;
}
```

## Long class (long.c)

`Long_alloc`, `Long_allocArray`, and `Long_allocWithValue` are the low-level
allocation functions behind `Long(...)` and `Long_array(...)`; examples use
those preferred macro forms. `Long_init` and `Long_shutdown` manage the backing
pool lifecycle, but
`_init()` calls are excluded from cookbook examples. Pool bootstrap and teardown
remain lifecycle gaps; `Long(...)` is the value constructor.

```c
#include "primitive/long.h"

int main(void)
{
    void *value = Long(9000000LL);
    void *values = Long_array(4u);
    int64_t longValue = Long_get(value);
    Long_set(value, 9000001LL);
    bool compareAndSet = Long_compareAndSet(value, 9000001LL, 9000002LL);
    uint64_t valueType = Long_type(value);
    size_t valueLength = Long_length(value);
    Long_free(values);
    Long_free(value);
    return 0;
}
```

## Float class (float.c)

`Float_alloc`, `Float_allocArray`, and `Float_allocWithValue` are the low-level
allocation functions behind `Float(...)` and `Float_array(...)`; examples use
those preferred macro forms. `Float_init` and `Float_shutdown` manage the
backing pool lifecycle, but
`_init()` calls are excluded from cookbook examples. Pool bootstrap and teardown
remain lifecycle gaps; `Float(...)` is the value constructor.

```c
#include "primitive/float.h"

int main(void)
{
    void *value = Float(0.5f);
    void *values = Float_array(4u);
    float floatValue = Float_get(value);
    Float_set(value, 0.75f);
    bool compareAndSet = Float_compareAndSet(value, 0.75f, 1.0f);
    uint64_t valueType = Float_type(value);
    size_t valueLength = Float_length(value);
    Float_free(values);
    Float_free(value);
    return 0;
}
```

## Double class (double.c)

`Double_alloc`, `Double_allocArray`, and `Double_allocWithValue` are the low-level
allocation functions behind `Double(...)` and `Double_array(...)`; examples use
those preferred macro forms. `Double_init` and `Double_shutdown` manage the
backing pool lifecycle, but
`_init()` calls are excluded from cookbook examples. Pool bootstrap and teardown
remain lifecycle gaps; `Double(...)` is the value constructor.

```c
#include "primitive/double.h"

int main(void)
{
    void *value = Double(0.125);
    void *values = Double_array(4u);
    double doubleValue = Double_get(value);
    Double_set(value, 0.25);
    bool compareAndSet = Double_compareAndSet(value, 0.25, 0.5);
    uint64_t valueType = Double_type(value);
    size_t valueLength = Double_length(value);
    Double_free(values);
    Double_free(value);
    return 0;
}
```

## Brain class (brain.c)

`Brain_alloc`, `Brain_allocArray`, and `Brain_allocWithValue` are the low-level
allocation functions behind `Brain(...)` and `Brain_array(...)`; examples use
those preferred macro forms. `Brain_init` and `Brain_shutdown` manage the
backing pool lifecycle, but
`_init()` calls are excluded from cookbook examples. Pool bootstrap and teardown
remain lifecycle gaps; `Brain(...)` is the value constructor.

```c
#include "primitive/brain.h"

int main(void)
{
    uint16_t initialBrainBits = Brain_floatToBFloat16(3.5f);
    void *value = Brain(initialBrainBits);
    void *values = Brain_array(4u);
    uint16_t brainValue = Brain_get(value);
    uint16_t updatedBrainBits = Brain_floatToBFloat16(2.5f);
    Brain_set(value, updatedBrainBits);
    bool compareAndSet = Brain_compareAndSet(value, 0u, 1u);
    uint64_t valueType = Brain_type(value);
    size_t valueLength = Brain_length(value);
    uint16_t brainFloatBits = Brain_floatToBFloat16(3.5f);
    float decodedFloat = Brain_bFloat16ToFloat(0x4060u);
    float brainFloat = Brain_getFloat(value);
    Brain_setFloat(value, 3.5f);
    Brain_free(values);
    Brain_free(value);
    return 0;
}
```

## Fixed32 class (fixed32.c)

`Fixed32_alloc`, `Fixed32_allocArray`, and `Fixed32_allocWithValue` are the
low-level allocation functions behind `Fixed32(...)` and `Fixed32_array(...)`;
examples use those preferred macro forms. `Fixed32_init` and `Fixed32_shutdown`
manage the backing pool lifecycle, but
`_init()` calls are excluded from cookbook examples. Pool bootstrap and teardown
remain lifecycle gaps; `Fixed32(...)` is the value constructor.

```c
#include "primitive/fixed32.h"

int main(void)
{
    void *value = Fixed32(81920);
    void *values = Fixed32_array(4u);
    int32_t fixedValue = Fixed32_get(value);
    Fixed32_set(value, 98304);
    bool compareAndSet = Fixed32_compareAndSet(value, 98304, 131072);
    uint64_t valueType = Fixed32_type(value);
    size_t valueLength = Fixed32_length(value);
    Fixed32_free(values);
    Fixed32_free(value);
    return 0;
}
```

## Fixed64 class (fixed64.c)

`Fixed64_alloc`, `Fixed64_allocArray`, and `Fixed64_allocWithValue` are the
low-level allocation functions behind `Fixed64(...)` and `Fixed64_array(...)`;
examples use those preferred macro forms. `Fixed64_init` and `Fixed64_shutdown`
manage the backing pool lifecycle, but
`_init()` calls are excluded from cookbook examples. Pool bootstrap and teardown
remain lifecycle gaps; `Fixed64(...)` is the value constructor.

```c
#include "primitive/fixed64.h"

int main(void)
{
    void *value = Fixed64(163840LL);
    void *values = Fixed64_array(4u);
    int64_t fixedValue = Fixed64_get(value);
    Fixed64_set(value, 196608LL);
    bool compareAndSet = Fixed64_compareAndSet(value, 196608LL, 262144LL);
    uint64_t valueType = Fixed64_type(value);
    size_t valueLength = Fixed64_length(value);
    Fixed64_free(values);
    Fixed64_free(value);
    return 0;
}
```

## IntFloat class (int_float.c)

`IntFloat_alloc`, `IntFloat_allocArray`, and `IntFloat_allocWithValues` are the
low-level allocation functions behind `IntFloat(...)` and `IntFloat_array(...)`;
examples use those preferred macro forms. `IntFloat_init` and `IntFloat_shutdown`
manage the backing pool lifecycle, but
`_init()` calls are excluded from cookbook examples. Pool bootstrap and teardown
remain lifecycle gaps; `IntFloat(...)` is the value constructor.

```c
#include "primitive/int_float.h"

int main(void)
{
    void *value = IntFloat(9000, 0.25f);
    void *values = IntFloat_array(4u);
    int64_t integerValue = IntFloat_get(value);
    IntFloat_set(value, 9001);
    bool compareAndSet = IntFloat_compareAndSet(value, 9001, 9002);
    uint64_t valueType = IntFloat_type(value);
    size_t valueLength = IntFloat_length(value);
    IntFloat_free(values);
    IntFloat_free(value);
    return 0;
}
```

## IntDouble class (int_double.c)

`IntDouble_alloc`, `IntDouble_allocArray`, and `IntDouble_allocWithValues` are the
low-level allocation functions behind `IntDouble(...)` and `IntDouble_array(...)`;
examples use those preferred macro forms. `IntDouble_init` and `IntDouble_shutdown`
manage the backing pool lifecycle, but
`_init()` calls are excluded from cookbook examples. Pool bootstrap and teardown
remain lifecycle gaps; `IntDouble(...)` is the value constructor.

```c
#include "primitive/int_double.h"

int main(void)
{
    void *value = IntDouble(9000, 0.25);
    void *values = IntDouble_array(4u);
    int64_t integerValue = IntDouble_get(value);
    IntDouble_set(value, 9001);
    bool compareAndSet = IntDouble_compareAndSet(value, 9001, 9002);
    uint64_t valueType = IntDouble_type(value);
    size_t valueLength = IntDouble_length(value);
    IntDouble_free(values);
    IntDouble_free(value);
    return 0;
}
```

## LongFloat class (long_float.c)

`LongFloat_alloc`, `LongFloat_allocArray`, and `LongFloat_allocWithValues` are the
low-level allocation functions behind `LongFloat(...)` and `LongFloat_array(...)`;
examples use those preferred macro forms. `LongFloat_init` and `LongFloat_shutdown`
manage the backing pool lifecycle, but
`_init()` calls are excluded from cookbook examples. Pool bootstrap and teardown
remain lifecycle gaps; `LongFloat(...)` is the value constructor.

```c
#include "primitive/long_float.h"

int main(void)
{
    void *value = LongFloat(9000000LL, 0.5f);
    void *values = LongFloat_array(4u);
    int64_t integerValue = LongFloat_get(value);
    LongFloat_set(value, 9000001LL);
    bool compareAndSet = LongFloat_compareAndSet(value, 9000001LL, 9000002LL);
    uint64_t valueType = LongFloat_type(value);
    size_t valueLength = LongFloat_length(value);
    LongFloat_free(values);
    LongFloat_free(value);
    return 0;
}
```

## LongDouble class (long_double.c)

`LongDouble_alloc`, `LongDouble_allocArray`, and `LongDouble_allocWithValues` are
the low-level allocation functions behind `LongDouble(...)` and
`LongDouble_array(...)`; examples use those preferred macro forms.
`LongDouble_init` and `LongDouble_shutdown` manage the backing pool lifecycle,
but `_init()` calls are excluded from cookbook examples. Pool bootstrap and
teardown remain lifecycle gaps; `LongDouble(...)` is the value constructor.

```c
#include "primitive/long_double.h"

int main(void)
{
    void *value = LongDouble(9000000LL, 0.5);
    void *values = LongDouble_array(4u);
    int64_t integerValue = LongDouble_get(value);
    LongDouble_set(value, 9000001LL);
    bool compareAndSet = LongDouble_compareAndSet(value, 9000001LL, 9000002LL);
    uint64_t valueType = LongDouble_type(value);
    size_t valueLength = LongDouble_length(value);
    LongDouble_free(values);
    LongDouble_free(value);
    return 0;
}
```

## String class (string.c)

`String_appendInto` still accepts a caller-provided destination. `String_append`
and `String_appendLiteral` already return their produced blocks; `appendInto`
remains a migration gap.

```c
#include "primitive/string.h"

int main(void)
{
    const uint8_t searchValue[] = "player";
    const uint8_t suffixValue[] = "name";
    uint8_t *label = String("player-name-goes-here");
    uint8_t *copy = String(label);
    uint8_t *combined = String("combined-string-goes-here");
    const char *stringValue = String_get(label);
    size_t stringLength = String_length(label);
    uint64_t stringType = String_type(label);
    bool isArray = String_isArray(label);
    uint32_t classId = String_classId();
    size_t stringCapacity = String_capacity(label);
    uint8_t *stringCopy = String_copy(label);
    bool stringsEqual = String_equals(label, "player-name-goes-here");
    int comparison = String_compare(label, copy);
    bool containsValue = String_contains(label, searchValue);
    bool containsLiteral = String_containsLiteral(label, "player");
    int64_t valueIndex = String_indexOf(label, searchValue);
    int64_t literalIndex = String_indexOfLiteral(label, "player");
    bool isInString = String_instring(0u, label, searchValue);
    bool isLiteralInString = String_instringLiteral(0u, label, "player");
    uint8_t *substring = String_substring(label, 0u, 6u);
    uint8_t *literalSubstring = String_substringLiteral("player-name-goes-here", 0u, 6u);
    uint8_t *firstCharacter = String_subFirstChar(label);
    uint8_t *lastCharacter = String_subLastChar(label);
    uint8_t *prefix = String_subFirst(label, 6u);
    uint8_t *suffix = String_subLast(label, 4u);
    uint8_t *appended = String_append(label, suffixValue);
    uint8_t *appendedLiteral = String_appendLiteral(label, "suffix-goes-here");
    uint8_t *literals = String_appendLiterals("prefix-goes-here", "suffix-goes-here");
    uint8_t *appendedFirst = String_appendFirst(label, suffixValue);
    uint8_t *appendedFirstLiteral = String_appendFirstLiteral(label, "suffix-goes-here");
    String_free(stringCopy);
    String_free(substring);
    String_free(literalSubstring);
    String_free(prefix);
    String_free(suffix);
    String_free(appended);
    String_free(appendedLiteral);
    String_free(literals);
    String_free(appendedFirst);
    String_free(appendedFirstLiteral);
    String_free(combined);
    String_free(copy);
    String_free(label);
    return 0;
}
```

## Pack class (pack.h)

```c
#include "primitive/pack.h"

int main(void)
{
    int16_t packedBytes = Pack_packByte(7, 42);
    int32_t packedShorts = Pack_packShort(7, 42);
    int64_t packedInts = Pack_packInt(7, 42);
    int8_t firstByte = Pack_unpackByte1(packedBytes);
    int8_t secondByte = Pack_unpackByte2(packedBytes);
    int16_t firstShort = Pack_unpackShort1(packedShorts);
    int16_t secondShort = Pack_unpackShort2(packedShorts);
    int32_t firstInt = Pack_unpackInt1(packedInts);
    int32_t secondInt = Pack_unpackInt2(packedInts);
    return 0;
}
```

## Choice class (choice.c)

```c
#include "objects/choice.h"

int main(void)
{
    Choice *choice = Choice(nullptr, nullptr, 0u);
    uint32_t choiceLength = Choice_length(choice);
    uint64_t chosenObject = Choice_getObject(choice, 0u);
    Choice_trigger(choice, 0u, nullptr);
    Choice_free(choice);
    return 0;
}
```

## Future class (future.c)

```c
#include "objects/future.h"

int main(void)
{
    Future *future = Future();
    bool isGiven = Future_isGiven(future);
    uint64_t result = Future_get(future);
    bool desiredValueSet = Future_setDesiredValue(future, 42u);
    Future_free(future);
    return 0;
}
```

## Global class (global.c)

```c
#include "objects/global.h"

int main(void)
{
    Global *sharedValue = Global(7u);
    uint64_t sharedInteger = Global_get(sharedValue);
    Global_set(sharedValue, 8u);
    bool compareAndSet = Global_compareAndSet(sharedValue, 8u, 9u);
    Global_free(sharedValue);
    return 0;
}
```

## Local class (local.c)

```c
#include "objects/local.h"

int main(void)
{
    Local *threadValue = Local();
    uint64_t threadInteger = Local_get(threadValue, 0u);
    Local_set(threadValue, 0u, 7u);
    Local_free(threadValue);
    return 0;
}
```

## Passive class (passive.c)

```c
#include "objects/passive.h"

int main(void)
{
    Passive *value = Passive(nullptr, nullptr, nullptr);
    uint64_t passiveValue = Passive_get(value);
    Passive_set(value, 7u);
    Passive_free(value);
    return 0;
}
```

## Probable class (probable.c)

```c
#include "objects/probable.h"

int main(void)
{
    Probable *item = Probable(501u, 1u, 3u);
    uintptr_t object = Probable_object(item);
    uint32_t weight = Probable_weight(item);
    uint32_t totalWeight = Probable_total(item);
    Probable_setObject(item, 502u);
    Probable_setWeight(item, 2u);
    Probable_setTotal(item, 4u);
    uintptr_t selectedObject = Probable_get(item);
    Probable_free(item);
    return 0;
}
```

## ProbableObjects class (probable_objects.c)

```c
#include "objects/probable_objects.h"

int main(void)
{
    ProbableObjects *pool = ProbableObjects(8u);
    Probable *item = Probable(501u, 1u, 3u);
    size_t itemCount = ProbableObjects_size(pool);
    size_t itemCapacity = ProbableObjects_capacity(pool);
    uint32_t totalWeight = ProbableObjects_totalWeight(pool);
    int add = ProbableObjects_add(pool, 502u, 2u);
    int addProbable = ProbableObjects_addProbable(pool, item);
    uintptr_t object = ProbableObjects_objectAt(pool, 0u);
    uint32_t cumulativeWeight = ProbableObjects_cumulativeAt(pool, 0u);
    uint32_t itemWeight = ProbableObjects_weightAt(pool, 0u);
    uintptr_t selectedObject = ProbableObjects_get(pool);
    Probable_free(item);
    ProbableObjects_free(pool);
    return 0;
}
```

## ReactiveInt class (reactive_primitive.c)

This implementation stamps the scalar reactive family.

```c
#include "reactive/reactive.h"
#include "reactive/reactive_primitive.h"
#include "reactive/generic.h"

int main(void)
{
    ReactiveInt *score = ReactiveInt(0);
    ReactiveInt_set(score, 10);
    int scoreValue = ReactiveInt_get(score);
    ReactiveInt_free(score);
    return 0;
}
```

## Variable class (variable.c)

`Variable(...)` allocates and initializes the object internally; callers use the
constructor macro shown below rather than the lower-level initializer.
`Variable_toString` and `Variable_toStringStruct` take caller-provided
destinations and remain Value Return Law migration gaps. `Variable_read` and
`Variable_setRead` need a real `VariableReadFn`, which this one-main cookbook
format cannot define.

```c
#include "reflection/variable.h"

int main(void)
{
    Variable *value = Variable("variable-name-goes-here");
    const char *name = Variable_getName(value);
    uint64_t variableKind = Variable_kind(value);
    bool hasVariableType = Variable_check(value, 0u);
    bool nameSet = Variable_setName(value, "renamed-variable-goes-here");
    VariableReadFn readFunction = Variable_getRead(value);
    Variable_setTarget(value, nullptr);
    void *target = Variable_getTarget(value);
    Variable_free(value);
    return 0;
}
```

## Field class (field.c)

`Field(...)` allocates and initializes the object internally; callers use the
constructor macro shown below rather than the lower-level initializer.
`Field_toString` and `Field_toStringStruct` take caller-provided destinations
and remain Value Return Law migration gaps. `Field_read`, `Field_write`,
`Field_setRead`, and `Field_setSet` need real reader and writer callbacks,
which this one-main cookbook format cannot define.

```c
#include "reflection/field.h"

int main(void)
{
    Field *field = Field("field-name-goes-here");
    const char *name = Field_getName(field);
    uint64_t fieldKind = Field_kind(field);
    bool fieldHasType = Field_check(field, 0u);
    Variable *variable = Field_getVariable(field);
    bool nameSet = Field_setName(field, "renamed-field-goes-here");
    VariableReadFn readFunction = Field_getRead(field);
    FieldSetFn setFunction = Field_getSet(field);
    Field_setTarget(field, nullptr);
    void *target = Field_getTarget(field);
    Field_setTypeId(field, 0u);
    uint64_t typeId = Field_getTypeId(field);
    Field_setOffset(field, 0u);
    uint32_t offset = Field_getOffset(field);
    Field_setSize(field, 0u);
    uint32_t size = Field_getSize(field);
    Field_setFlags(field, REFLECT_FIELD_NONE);
    uint32_t flags = Field_getFlags(field);
    bool isNullable = Field_isNullable(field);
    bool isKey = Field_isKey(field);
    bool isIndexed = Field_isIndexed(field);
    Field_free(field);
    return 0;
}
```

## Method class (method.c)

`Method(...)` allocates and initializes the object internally; callers use the
constructor macro shown below rather than the lower-level initializer.
`Method_toString` and `Method_toStringStruct` take caller-provided destinations
and remain Value Return Law migration gaps. `Method_call` and
`Method_setInvoke` need a real `MethodFn`, which this one-main cookbook format
cannot define.

```c
#include "reflection/method.h"

int main(void)
{
    Method *method = Method("method-name-goes-here");
    const char *name = Method_getName(method);
    uint64_t methodKind = Method_kind(method);
    bool methodHasType = Method_check(method, 0u);
    bool nameSet = Method_setName(method, "renamed-method-goes-here");
    MethodFn invoke = Method_getInvoke(method);
    Method_setTarget(method, nullptr);
    void *target = Method_getTarget(method);
    Method_free(method);
    return 0;
}
```

## Struct class (struct.c)

`Struct(...)` allocates and initializes the object internally; callers use the
constructor macro shown below rather than the lower-level initializer.
The string projections still take caller-provided destinations and remain
Value Return Law migration gaps (`Struct_toString` and
`Struct_toStringStruct`). `Struct_forEach` requires a callback function.

```c
#include "reflection/struct.h"

int main(void)
{
    Struct *schema = Struct("entity-name-goes-here");
    const char *name = Struct_getName(schema);
    Field *field = Field("field-name-goes-here");
    uint64_t structKind = Struct_kind(schema);
    bool structHasType = Struct_check(schema, 0u);
    uint32_t fieldIndex = Struct_add(schema, field);
    Field *firstField = Struct_get(schema, 0u);
    bool nameSet = Struct_setName(schema, "renamed-entity-goes-here");
    Struct_setSize(schema, 4u);
    uint32_t layoutSize = Struct_getSize(schema);
    uint32_t fieldCount = Struct_count(schema);
    bool isEmpty = Struct_isEmpty(schema);
    Struct_free(schema);
    Field_free(field);
    return 0;
}
```

## Class class (class.c)

`Class(...)` allocates and initializes the object internally; callers use the
constructor macro shown below rather than the lower-level initializer.
`Class_toString` and `Class_toStringStruct` take caller-provided destinations
and remain Value Return Law migration gaps. Construction requires a real
constructor callback, and `Class_forEachMethod` requires a visitor callback;
this one-main cookbook format cannot define those functions.

```c
#include "reflection/class.h"

int main(void)
{
    Struct *layout = Struct("class-layout-goes-here");
    Class *classInfo = Class("class-name-goes-here", layout);
    const char *name = Class_getName(classInfo);
    Method *method = Method("method-name-goes-here");
    uint64_t classKind = Class_kind(classInfo);
    bool classHasType = Class_check(classInfo, 0u);
    Struct *classLayout = Class_getLayout(classInfo);
    Class_setLayout(classInfo, layout);
    ClassConstructFn construct = Class_getConstruct(classInfo);
    uint32_t addMethod = Class_addMethod(classInfo, method);
    Method *firstMethod = Class_getMethod(classInfo, 0u);
    uint32_t methodCount = Class_methodCount(classInfo);
    bool nameSet = Class_setName(classInfo, "renamed-class-goes-here");
    Class_free(classInfo);
    Struct_free(layout);
    Method_free(method);
    return 0;
}
```

## Regex class (regex.c)

`Regex_find` and `Regex_findGroups` write matches to caller storage, while the
string projections require destinations. Those functions are Value Return Law
migration gaps and are omitted here.

```c
#include "regex/regex.h"

int main(void)
{
    Regex *pattern = Regex("[A-Za-z_][A-Za-z0-9_]*");
    Regex_pattern(pattern);
    uint32_t flags = Regex_flags(pattern);
    uint32_t groupCount = Regex_groupCount(pattern);
    uint32_t instCount = Regex_instCount(pattern);
    uint32_t classCount = Regex_classCount(pattern);
    bool hasMatch = Regex_isMatch(pattern, "player_name");
    bool isFullMatch = Regex_isFullMatch(pattern, "player_name");
    Regex_free(pattern);
    return 0;
}
```

## RegexOptions class (vm.h)

`RegexOptions(...)` constructs the value record; its public setters change each
option without writing fields directly.

```c
#include "regex/vm.h"

int main(void)
{
    RegexOptions options = RegexOptions(false, false, false);
    RegexOptions_setIgnoreCase(&options, true);
    RegexOptions_setDotall(&options, true);
    RegexOptions_setMultiline(&options, true);
    return 0;
}
```

## SymbolTable class (symbol_table.c)

`SymbolTable_findByClass` writes IDs to a caller-provided buffer and remains a
Value Return Law migration gap. Relational Engine must initialize its memory
owner and shared variable pool before this example runs.

```c
#include "relational/symbol_table.h"

int main(void)
{
    SymbolTable symbols = SymbolTable();
    int32_t variableId = SymbolTable_instant(&symbols, "player-health", 1u, 42u);
    bool rename = SymbolTable_rename(&symbols, "player-health", "player-vitality");
    int32_t renamedVariableId = SymbolTable_getId(&symbols, "player-vitality");
    uintptr_t variablePointer = SymbolTable_getPointer(&symbols, variableId);
    SymbolTable_setPointer(&symbols, variableId, 43u);
    bool compareAndSetPointer = SymbolTable_compareAndSetPointer(&symbols, variableId, 43u, 44u);
    uint32_t variableClassId = SymbolTable_getClassId(&symbols, variableId);
    const char *variableName = SymbolTable_getName(&symbols, variableId);
    size_t activeVariableCount = SymbolTable_getActiveCount(&symbols);
    SymbolTable_shutdown(&symbols);
    return 0;
}
```

## Cell class (cell.c)

`Cell_toString` and `Cell_toStringStruct` take caller-provided destinations
and remain Value Return Law migration gaps.

```c
#include "relational/cell.h"

int main(void)
{
    Cell *cell = Cell(0u, 42u);
    uint64_t typeId = Cell_typeId(cell);
    bool check = Cell_check(cell, 0u);
    Cell_setValue(cell, 43u);
    uintptr_t value = Cell_getValue(cell);
    Cell_free(cell);
    return 0;
}
```

## Relational class (relational.c)

`Relational_search` and `Relational_searchAll` write result IDs to
caller-provided buffers and remain Value Return Law migration gaps.

```c
#include "relational/relational.h"

int main(void)
{
    SymbolTable scope = SymbolTable();
    SymbolTable global = SymbolTable();
    int32_t instant = SymbolTable_instant(&scope, "player-health", 1u, 42u);
    int32_t variableId = Relational_getId(&scope, "player-health");
    const char *variableName = Relational_getName(&scope, 0);
    bool nameSet = Relational_setName(&scope, "player-health", "player-vitality");
    void *variableValue = Relational_getValue(&scope, "player-vitality");
    void *valueById = Relational_getValueById(&scope, 0);
    bool valueSet = Relational_setValue(&scope, "player-vitality", 1u, (void*) 43u);
    bool valueByIdSet = Relational_setValueById(&scope, 0, (void*) 44u);
    const char *stringValue = Relational_getString(&scope, "missing-string-name");
    Relational_setString(&scope, "display-name", "name-goes-here");
    void *functionValue = Relational_getFunction(&scope, "missing-function-name");
    bool functionSet = Relational_setFunction(&scope, "function-name", nullptr);
    SymbolTable_shutdown(&scope);
    SymbolTable_shutdown(&global);
    return 0;
}
```

## Shelf class (shelf.c)

`Shelf()` allocates and initializes the object internally; callers use the
constructor macro shown below rather than the lower-level initializer.
`Shelf_toString` and `Shelf_toStringStruct` take caller-provided destinations
and remain Value Return Law migration gaps. `Shelf_init` is the lower-level
initializer already used by `Shelf()`; the example uses the preferred macro.

```c
#include "relational/shelf.h"

int main(void)
{
    Shelf *shelf = Shelf();
    uint32_t first = Shelf_addCell(shelf, 1u, 42u);
    uint32_t second = Shelf_addNode(shelf, 0u);
    uintptr_t cell = Shelf_getCell(shelf, first);
    uint32_t next = Shelf_getNext(shelf, first);
    bool nextSet = Shelf_setNext(shelf, first, second);
    bool link = Shelf_link(shelf, first, second);
    bool headSet = Shelf_setHead(shelf, first);
    uint32_t head = Shelf_getHead(shelf);
    uint32_t nodeCount = Shelf_count(shelf);
    bool isEmpty = Shelf_isEmpty(shelf);
    Shelf_free(shelf);
    return 0;
}
```

## ComputeThread class (compute.c)

The constructor and context setter configure job state without initializing
fields directly. Defining executable callbacks requires a helper outside this
one-main example, so `ComputeJob_setRun`, `ComputeJob_setOnDone`,
`ComputeJob_run`, `ComputeThread_submit`, and `ComputeThread_submitTo` remain
callback callability gaps.

```c
#include "thread/compute.h"

int main(void)
{
    int jobContext = 73;
    ComputeJob job = ComputeJob(nullptr, &jobContext, nullptr);
    ComputeJob_setContext(&job, &jobContext);
    bool isJob = ComputeJob_isJob(&job);

    Thread *worker = ComputeThread_invoke();
    bool start = ComputeThread_start(1u);
    size_t workerCount = ComputeThread_count();
    ComputeThread_stop();
    ComputeThread_free();
    Thread_stop(worker);
    Thread_free(worker);
    return 0;
}
```

## Thread class (thread.c)

`Thread` construction requires a `Thread_Job` callback, which cannot be
defined in the cookbook's one-main format. `Thread_run`, `Thread_submit`,
`Thread_stop`, `Thread_free`, `Thread_isRunning`, `Thread_queue`, and
`Thread_purpose` all require that unavailable instance, so those calls remain
constructor/callback gaps. The registry-wide `Thread_runAll`,
`Thread_stopAll`, `Thread_count`, `Thread_freeAll`, and
`Thread_freeAllSystem` calls need no instance and are shown below.

```c
#include "thread/thread.h"

int main(void)
{
    Thread_runAll();
    Thread_stopAll();
    size_t threadCount = Thread_count();
    Thread_freeAll();
    Thread_freeAllSystem();
    return 0;
}
```

## EventThread class (event.c)

`EventThread_submit` needs a non-null packet, but the public event packet has
no constructor/setter API. A `ComputeJob` payload would need a run callback
that this one-main example cannot define, and the current event job ignores
custom packets.

```c
#include "thread/event.h"
int main(void)
{
    Thread *events = EventThread_invoke();
    EventThread_stop(events);
    EventThread_free(events);
    return 0;
}
```

## NetworkingThread class (networking.c)

`NetworkingThread_submit` needs a non-null batch payload. The current worker
accepts an opaque batch pointer but the cookbook has no public batch
constructor to supply one. A `ComputeJob` payload would need a run callback
that this one-main example cannot define.

```c
#include "thread/networking.h"
int main(void)
{
    Thread *network = NetworkingThread_invoke();
    Thread *core = NetworkingThread_core();
    NetworkingThread_stop(network);
    NetworkingThread_free(network);
    return 0;
}
```

## ScriptingThread class (scripting.c)

`ScriptingThread_submit` needs a non-null task payload, for which the public
API has no constructor in this example. A `ComputeJob` payload would need a
run callback that this one-main example cannot define.

```c
#include "thread/scripting.h"
int main(void)
{
    Thread *scripts = ScriptingThread_invoke();
    ScriptingThread_stop(scripts);
    ScriptingThread_free(scripts);
    return 0;
}
```

## UIThread class (ui.c)

`UIThread_submit` needs a non-null packet payload, for which the public API
has no constructor in this example. A `ComputeJob` payload would need a run
callback that this one-main example cannot define.

```c
#include "thread/ui.h"
int main(void)
{
    Thread *ui = UIThread_invoke();
    UIThread_stop(ui);
    UIThread_free(ui);
    return 0;
}
```

## ReactiveThread class (thread/reactive.c)

`ReactiveThread_wake`, `ReactiveThread_wakeOn`, `ReactiveThread_adopt`,
`ReactiveThread_release`, and `ReactiveThread_isQueued` need a constructed
`Reactive` instance. Its preferred constructor is currently unavailable, so
those box-bound calls remain API gaps.

```c
#include "thread/reactive.h"
int main(void)
{
    Thread *worker = ReactiveThread_invoke();
    Thread *sharedWorker = ReactiveThread_core();
    bool start = ReactiveThread_start();
    size_t pendingCount = ReactiveThread_pending();
    ReactiveThread_stop(worker);
    ReactiveThread_free(worker);
    ReactiveThread_shutdown();
    return 0;
}
```

## Reactive class (reactive/reactive.c)

The bare `Reactive(...)` constructor macro is retired, and its replacement
constructor is not available for an untyped engine. `Reactive_1`, `Reactive_2`,
and `Reactive_init` are constructor arms/initializers rather than the preferred
macro, so instance-bound calls remain blocked until `Reactive()` is restored.
That blocks `Reactive_free`, `Reactive_shutdown`, `Reactive_load`,
`Reactive_store`, `Reactive_setDelivery`, `Reactive_clearDelivery`,
`Reactive_getDelivery`, `Reactive_setValueOf`, `Reactive_drain`,
`Reactive_observerCount`, `Reactive_isDirty`, and `Reactive_isActive`.
`Reactive_watchSet`, `Reactive_unwatchSet`, `Reactive_watchChanged`,
`Reactive_unwatchChanged`, `Reactive_watchGet`, `Reactive_unwatchGet`,
`Reactive_watchNullptr`, and `Reactive_unwatchNullptr` also need a constructed
instance and callback values. `Reactive_valueOf` additionally writes into a
caller-provided output buffer and is a Value Return Law gap. The process default
delivery setter and getter work without an instance; the getter result is stored
as a value and is not invoked.

```c
#include "reactive/reactive.h"

int main(void)
{
    Reactive_setDefaultDelivery(nullptr);
    ReactiveDeliverFn defaultDelivery = Reactive_getDefaultDelivery();
    return 0;
}
```

## DrawThread class (draw.c)

`DrawThread_submitTo` needs a live draw task, usually a `ComputeJob` whose run
callback must be defined outside this one-main example. The role worker is
created by `DrawThread_invokeRole`, but a valid task cannot be constructed here,
so submission remains a callback callability gap.

```c
#include "thread/draw.h"
int main(void)
{
    Thread *sceneThread = DrawThread_invokeRole(DRAW_ROLE_SCENE);
    DrawThread_stopAll();
    DrawThread_freeAll();
    return 0;
}
```

## SecureRandom class (secure_random.c)

`SecureRandom_bytes` fills a caller buffer and remains a Value Return Law
migration gap; scalar draws return directly.

```c
#include "security/secure_random.h"

int main(void)
{
    SecureRandom *random = SecureRandom();
    uint64_t u64 = SecureRandom_u64(random);
    uint32_t u32 = SecureRandom_u32(random);
    uint64_t draws = SecureRandom_draws(random);
    SecureRandom_free(random);
    return 0;
}
```

## Base32 class (base32.c)

`Base32_encode` and `Base32_decode` write caller buffers and output values
through pointers, so both remain Value Return Law gaps. The length queries
return values directly.

```c
#include "security/base32.h"

int main(void)
{
    size_t encodedLength = Base32_encodedLength(20u);
    size_t decodedLength = Base32_decodedLength(32u);
    return 0;
}
```

## Hmac class (hmac.c)

`Hmac_sha1` and `Hmac_sha256` write digest bytes into caller buffers; they
remain Value Return Law migration gaps.

```c
#include "security/hmac.h"

int main(void)
{
    return 0;
}
```

## CryptoSha1 class (sha1.c)

`Crypto_sha1` and `Crypto_sha1Final` write digest bytes to caller buffers and
remain Value Return Law migration gaps. The streaming context has a constructor
macro, so initialization and update calls are shown; finalization still needs a
caller-owned digest buffer.

```c
#include "security/sha1.h"

int main(void)
{
    CryptoSha1 sha1 = CryptoSha1();
    Crypto_sha1Init(&sha1);
    Crypto_sha1Update(&sha1, "message-goes-here", 17u);
    return 0;
}
```

## Totp class (totp.c)

`Totp_verify` takes an optional caller-provided replay-state pointer, so it
remains a Value Return Law migration gap even when replay tracking is disabled.

```c
#include "security/totp.h"

int main(void)
{
    const uint8_t secret[] = "api-secret-goes-here";
    uint32_t code = Totp_code(secret, sizeof secret, 1700000000u,
        TOTP_DIGITS_DEFAULT, TOTP_STEP_SECONDS_DEFAULT);
    return 0;
}
```

## OtpAuth class (otpauth.c)

`OtpAuth_buildUri` writes to a caller buffer and remains a Value Return Law
migration gap.

```c
#include "security/otpauth.h"

int main(void)
{
    return 0;
}
```

## Password class (password.c)

`Password_deriveSha1`, `Password_deriveSha256`, and
`Password_generateSalt` write results into caller-provided buffers and remain
Value Return Law migration gaps. `Password_verifySha256` returns a boolean
directly, so its result is assigned here.

```c
#include "security/password.h"

int main(void)
{
    const uint8_t salt[] = {0x01u, 0x02u, 0x03u, 0x04u};
    const uint8_t expectedKey[32] = {0};
    bool passwordMatches = Password_verifySha256(
        "password-goes-here", salt, sizeof salt, PASSWORD_ITERATIONS_MIN,
        expectedKey, sizeof expectedKey);
    return 0;
}
```

## Crypto class (crypto.c)

`Crypto_sha256Init` and `Crypto_sha256Update` need a `CryptoSha256` context,
which has no constructor macro. `Crypto_sha256Final`, `Crypto_sha256`,
`Crypto_sha256Hex`, `Crypto_toHex`, `Crypto_fromHex`, `Crypto_rngBytes`, and
`Crypto_prngBytes` write through caller-owned output buffers and remain Value
Return Law gaps. `CryptoRng` has no constructor macro, so
`Crypto_rngInit` and `Crypto_rngNextU64` are also unavailable as constructor-
compliant calls. The process-wide seed and scalar draw APIs return directly or
perform a direct state change and are shown below.

```c
#include "security/crypto.h"

int main(void)
{
    const char input[] = "hash-input-goes-here";
    bool constantTimeEquals = Crypto_constantTimeEquals(input, input, sizeof input);
    uint64_t hash64 = Crypto_hash64(input, sizeof input - 1u);
    uint32_t hash32 = Crypto_hash32(input, sizeof input - 1u);
    Crypto_prngSeed(1u);
    uint64_t prngU64 = Crypto_prngU64();
    return 0;
}
```

## Keychain class (keychain.c)

`Keychain_load` writes into caller-provided secret storage and remains a Value
Return Law migration gap.

```c
#include "security/keychain.h"

int main(void)
{
    bool isAvailable = Keychain_isAvailable();
    KeychainCode storeCode = Keychain_store("service-name-goes-here", "account-name-goes-here",
        (const uint8_t*) "api-secret-goes-here", 20u);
    KeychainCode remove = Keychain_remove("service-name-goes-here", "account-name-goes-here");
    const char *codeName = Keychain_codeName(KEYCHAIN_OK);
    return 0;
}
```

## TouchID class (touchid.c)

```c
#include "security/touchid.h"

int main(void)
{
    TouchIDToken token = TouchID_authenticate("Confirm this action");
    bool verify = TouchID_verify(token);
    TouchID_discard(token);
    TouchID_prompt("Confirm this action");
    return 0;
}
```

## System class (system.c)

```c
#include "system/system.h"

int main(void)
{
    System_initializeAll();
    bool environmentLoaded = System_getEnvironment("debug-env-path-goes-here", "export-env-path-goes-here");
    const char *environmentValue = System_getEnvValue("environment-name-goes-here");
    bool hasPath = System_hasEnv("PATH");
    System_freeEnvironment();
    return 0;
}
```

## DisplayInfo class (display_info.c)

`DisplayInfo_getMonitors` uses a caller-provided output count and remains a
Value Return Law migration gap.

```c
#include "system/display_info.h"

int main(void)
{
    int32_t monitorCount = DisplayInfo_getMonitorCount();
    DisplayInfo_setMonitorCount(1);
    DisplayMonitor *primary = DisplayInfo_getPrimaryMonitor();
    DisplayInfo_setPrimaryMonitor(primary);
    DisplayMonitor *monitor = DisplayInfo_getMonitor(0u);
    DisplayInfo_setMonitors(&primary, 1u);
    int32_t monitorWidth = DisplayInfo_getMonitorResolutionWidth();
    DisplayInfo_setMonitorResolutionWidth(1920);
    int32_t monitorHeight = DisplayInfo_getMonitorResolutionHeight();
    DisplayInfo_setMonitorResolutionHeight(1080);
    int32_t pointWidth = DisplayInfo_getPointResolutionWidth();
    DisplayInfo_setPointResolutionWidth(960);
    int32_t pointHeight = DisplayInfo_getPointResolutionHeight();
    DisplayInfo_setPointResolutionHeight(540);
    int32_t nativeWidth = DisplayInfo_getNativeResolutionWidth();
    DisplayInfo_setNativeResolutionWidth(1920);
    int32_t nativeHeight = DisplayInfo_getNativeResolutionHeight();
    DisplayInfo_setNativeResolutionHeight(1080);
    int32_t refreshRate = DisplayInfo_getCurrentRefreshRate();
    DisplayInfo_setCurrentRefreshRate(60);
    bool hdrSupported = DisplayInfo_getHdrSupported();
    DisplayInfo_setHdrSupported(false);
    float displayDensity = DisplayInfo_getDisplayDensity();
    DisplayInfo_setDisplayDensity(2.0f);
    float hardwareDensity = DisplayInfo_getHardwareDensity();
    DisplayInfo_setHardwareDensity(2.0f);
    return 0;
}
```

## DisplayMonitor class (display_monitor.c)

```c
#include "system/display_monitor.h"

int main(void)
{
    DisplayMonitor *monitor = DisplayMonitor();
    uint32_t monitorId = DisplayMonitor_getId(monitor);
    DisplayMonitor_setId(monitor, 1u);
    const char *monitorName = DisplayMonitor_getName(monitor);
    DisplayMonitor_setName(monitor, "monitor-name-goes-here");
    int32_t currentWidth = DisplayMonitor_getCurrentWidth(monitor);
    DisplayMonitor_setCurrentWidth(monitor, 1920);
    int32_t currentHeight = DisplayMonitor_getCurrentHeight(monitor);
    DisplayMonitor_setCurrentHeight(monitor, 1080);
    int32_t pointWidth = DisplayMonitor_getPointWidth(monitor);
    DisplayMonitor_setPointWidth(monitor, 960);
    int32_t pointHeight = DisplayMonitor_getPointHeight(monitor);
    DisplayMonitor_setPointHeight(monitor, 540);
    int32_t nativeWidth = DisplayMonitor_getNativeWidth(monitor);
    DisplayMonitor_setNativeWidth(monitor, 1920);
    int32_t nativeHeight = DisplayMonitor_getNativeHeight(monitor);
    DisplayMonitor_setNativeHeight(monitor, 1080);
    int32_t refreshRate = DisplayMonitor_getRefreshRate(monitor);
    DisplayMonitor_setRefreshRate(monitor, 60);
    bool hdrSupported = DisplayMonitor_getHdrSupported(monitor);
    DisplayMonitor_setHdrSupported(monitor, false);
    float dpi = DisplayMonitor_getDpi(monitor);
    DisplayMonitor_setDpi(monitor, 220.0f);
    DisplayMonitor_free(monitor);
    return 0;
}
```

## HardwareInfo class (hardware_info.c)

```c
#include "system/hardware_info.h"

int main(void)
{
    const char *operatingSystem = HardwareInfo_getOperatingSystem();
    HardwareInfo_setOperatingSystem("operating-system-name-goes-here");
    const char *architecture = HardwareInfo_getSystemArchitecture();
    HardwareInfo_setSystemArchitecture("architecture-name-goes-here");
    const char *deviceModel = HardwareInfo_getDeviceModel();
    HardwareInfo_setDeviceModel("device-model-goes-here");
    const char *cpuBrand = HardwareInfo_getCpuBrand();
    HardwareInfo_setCpuBrand("cpu-brand-goes-here");
    int32_t cpuCoreCount = HardwareInfo_getCpuCoreCount();
    HardwareInfo_setCpuCoreCount(8);
    int32_t cpuThreadCount = HardwareInfo_getCpuThreadCount();
    HardwareInfo_setCpuThreadCount(16);
    uint64_t ramTotal = HardwareInfo_getRamTotal();
    HardwareInfo_setRamTotal(16000000000u);
    uint64_t ramAvailable = HardwareInfo_getRamAvailable();
    HardwareInfo_setRamAvailable(8000000000u);
    uint64_t storageTotal = HardwareInfo_getStorageTotalSpace();
    HardwareInfo_setStorageTotalSpace(100000000000u);
    uint64_t storageAvailable = HardwareInfo_getStorageAvailableSpace();
    HardwareInfo_setStorageAvailableSpace(50000000000u);
    bool hasBattery = HardwareInfo_hasBattery();
    HardwareInfo_setHasBattery(true);
    float batteryLevel = HardwareInfo_getBatteryLevel();
    HardwareInfo_setBatteryLevel(0.75f);
    const char *batteryStatus = HardwareInfo_getBatteryStatus();
    HardwareInfo_setBatteryStatus("battery-status-goes-here");
    return 0;
}
```

## GraphicsInfo class (graphics_info.c)

```c
#include "system/graphics_info.h"

int main(void)
{
    const char *gpuName = GraphicsInfo_getGpuName();
    GraphicsInfo_setGpuName("gpu-name-goes-here");
    int32_t gpuVendorId = GraphicsInfo_getGpuVendorId();
    GraphicsInfo_setGpuVendorId(1);
    int32_t gpuDeviceId = GraphicsInfo_getGpuDeviceId();
    GraphicsInfo_setGpuDeviceId(2);
    const char *graphicsApi = GraphicsInfo_getPrimaryGraphicsApi();
    GraphicsInfo_setPrimaryGraphicsApi("graphics-api-name-goes-here");
    bool unifiedMemoryEnabled = GraphicsInfo_getUnifiedMemoryEnabled();
    GraphicsInfo_setUnifiedMemoryEnabled(true);
    bool computeShadersEnabled = GraphicsInfo_getComputeShadersEnabled();
    GraphicsInfo_setComputeShadersEnabled(true);
    bool meshShadersEnabled = GraphicsInfo_getMeshShadersEnabled();
    GraphicsInfo_setMeshShadersEnabled(false);
    bool hardwareRayTracingEnabled = GraphicsInfo_getHardwareRayTracingEnabled();
    GraphicsInfo_setHardwareRayTracingEnabled(false);
    int32_t maxTextureSize = GraphicsInfo_getMaxTextureSize();
    GraphicsInfo_setMaxTextureSize(8192);
    uint64_t vramTotal = GraphicsInfo_getVramTotal();
    GraphicsInfo_setVramTotal(8000000000u);
    uint64_t vramAvailable = GraphicsInfo_getVramAvailable();
    GraphicsInfo_setVramAvailable(4000000000u);
    return 0;
}
```

## AppDetect class (app_detect.c)

`AppDetect_which` writes a path to a caller buffer and remains a Value Return
Law migration gap.

```c
#include "system/app_detect.h"

int main(void)
{
    AppDetect *apps = AppDetect_shared();
    const AppSlot *editor = AppDetect_get(apps, "opencode");
    bool isOnPath = AppDetect_isOnPath(apps, "opencode");
    bool isBundle = AppDetect_isAppBundle(apps, "application-name-goes-here");
    bool isInstalled = AppDetect_isInstalled(apps, editor);
    bool isRunning = AppDetect_isRunning(apps, editor);
    uint32_t appCount = AppDetect_count(apps);
    const AppSlot *firstApp = AppDetect_at(apps, 0u);
    const char *name = AppDetect_getName(apps, editor);
    const char *alternateProcesses = AppDetect_getAltProcs(apps, editor);
    const char *displayName = AppDetect_getDisplayName(apps, editor);
    const char *note = AppDetect_getNote(apps, editor);
    return 0;
}
```

## CaptureTool class (capture_tool.c)

```c
#include "system/capture_tool.h"

int main(void)
{
    CaptureTool *tools = CaptureTool_shared();
    const CaptureSlot *recorder = CaptureTool_get(tools, "obs");
    uint32_t toolCount = CaptureTool_count(tools);
    const CaptureSlot *firstTool = CaptureTool_at(tools, 0u);
    bool isInstalled = CaptureTool_isInstalled(tools, recorder);
    bool isRunning = CaptureTool_isRunning(tools, recorder);
    uint32_t screenToolCount = CaptureTool_countRunning(tools, CAPTURE_KIND_SCREEN);
    uint32_t runningToolCount = CaptureTool_countRunningAll(tools);
    const char *slug = CaptureTool_getSlug(tools, recorder);
    const char *displayName = CaptureTool_getDisplayName(tools, recorder);
    const char *processKey = CaptureTool_getProcKey(tools, recorder);
    const char *driverDirectory = CaptureTool_getDriverDir(tools, recorder);
    CaptureKind kind = CaptureTool_getKind(tools, recorder);
    const char *note = CaptureTool_getNote(tools, recorder);
    return 0;
}
```

## ProcessProbe class (process_probe.c)

```c
#include "system/process_probe.h"

int main(void)
{
    const ProcessProbe *probe = ProcessProbe_shared();
    bool isRunning = ProcessProbe_isRunning(probe, "process-name-goes-here");
    bool isDriverLoaded = ProcessProbe_isDriverLoaded(probe, "plugin-directory-goes-here",
        "driver-name-prefix-goes-here");
    return 0;
}
```

## RegexCharClass class (charclass.c)

```c
#include "regex/charclass.h"

int main(void)
{
    RegexCharClass cls;
    RegexCharClass_clear(&cls);
    RegexCharClass_addByte(&cls, (uint8_t) 'a', true);
    RegexCharClass_addRange(&cls, (uint8_t) '0', (uint8_t) '9', false);
    RegexCharClass_addPredefined(&cls, 'w');
    bool isPredefined = RegexCharClass_isPredefined('d');
    RegexCharClass_negate(&cls);
    bool matchesByte = RegexCharClass_test(&cls, (uint8_t) 'A');
    return 0;
}
```

## RegexSpan class (span.c)

```c
#include "regex/span.h"

int main(void)
{
    RegexSpan span = RegexSpan_none();
    bool isSet = RegexSpan_isSet(span);
    size_t spanLength = RegexSpan_length(span);
    return 0;
}
```

## RegexNodeList class (nodelist.c)

```c
#include "regex/nodelist.h"

int main(void)
{
    RegexNodeList nodes = RegexNodeList();
    uint32_t index = RegexNodeList_add(&nodes, REGEX_NODE_CHAR);
    RegexNode *mutableNode = RegexNodeList_get(&nodes, index);
    const RegexNode *node = RegexNodeList_at(&nodes, index);
    RegexNodeList_free(&nodes);
    return 0;
}
```

## RegexProgram class (program.c)

```c
#include "regex/program.h"

int main(void)
{
    RegexNodeList nodes = RegexNodeList();
    uint32_t root = RegexNodeList_add(&nodes, REGEX_NODE_CHAR);
    RegexProgram program = RegexProgram();
    bool isBuilt = RegexProgram_build(&program, &nodes, root);
    uint32_t instructionCount = RegexProgram_count(&program);
    const RegexInst *instruction = RegexProgram_at(&program, 0u);
    RegexProgram_free(&program);
    RegexNodeList_free(&nodes);
    return 0;
}
```

## RegexParser class (parser.c)

`RegexParser_releaseClasses` requires an output count pointer. It remains a
Value Return Law migration gap, so the example does not transfer classes.

```c
#include "regex/parser.h"
#include <string.h>

int main(void)
{
    const char *pattern = "pattern-goes-here";
    RegexParser parser = RegexParser(pattern, strlen(pattern), false);
    uint32_t parsedRoot = RegexParser_parse(&parser);
    bool ok = RegexParser_ok(&parser);
    const char *parseError = RegexParser_error(&parser);
    RegexNodeList *nodes = RegexParser_nodes(&parser);
    uint32_t groupCount = RegexParser_groupCount(&parser);
    RegexParser_free(&parser);
    return 0;
}
```

## RegexVm class (vm.c)

```c
#include "regex/vm.h"

int main(void)
{
    RegexNodeList nodes = RegexNodeList();
    uint32_t root = RegexNodeList_add(&nodes, REGEX_NODE_CHAR);
    RegexProgram program = RegexProgram();
    bool isBuilt = RegexProgram_build(&program, &nodes, root);
    RegexVm vm = RegexVm(&program, 0u);
    RegexCharClass classes[1];
    RegexCharClass_clear(&classes[0]);
    RegexOptions options = RegexOptions(false, false, false);
    bool run = RegexVm_run(&vm, classes, "subject-goes-here", 16u, false, options);
    bool runFull = RegexVm_runFull(&vm, classes, "subject-goes-here", 16u, options);
    RegexSpan span = RegexVm_span(&vm, 0u);
    RegexVm_free(&vm);
    RegexProgram_free(&program);
    RegexNodeList_free(&nodes);
    return 0;
}
```

## Array class (array.c)

```c
#include "oop/type.h"
#include "struct/array.h"

int main(void)
{
    Array *array = Array(ID_INT, 4u);
    uint64_t firstValue = Array_get(array, 0u);
    Array_set(array, 0u, 42u);
    TryValue checkedValue = Array_getTry(array, 0u);
    uint8_t *firstSlot = Array_slot(array, 0u);
    bool isEmpty = Array_isEmpty(array);
    size_t itemCount = Array_size(array);
    size_t itemLength = Array_length(array);
    size_t itemCapacity = Array_capacity(array);
    uint32_t elementClassId = Array_elementClassId(array);
    size_t stride = Array_stride(array);
    uint8_t *arrayBuffer = Array_dataBuffer(array);
    Array_free(array);
    return 0;
}
```

## Collection class (collection.c)

`Collection` has no constructor; use an owning collection's embedded header.
Exhaustion reporting and unchecked slot operations are public APIs and shown
because they are part of the file's call surface.

```c
#include "oop/type.h"
#include "struct/array.h"

int main(void)
{
    Array *array = Array(ID_INT, 4u);
    Collection *collection = (Collection *) array;
    uint64_t collectionType = Collection_type(collection);
    uint32_t collectionSize = Collection_size(collection);
    uint32_t collectionLength = Collection_length(collection);
    bool isEmpty = Collection_isEmpty(collection);
    uint32_t elementClassId = Collection_elementClassId(collection);
    uint32_t keyClassId = Collection_keyClassId(collection);
    uint32_t stride = Collection_stride(collection);
    uint32_t valueClassId = Collection_valClassId(collection);
    uint32_t capacity = Collection_capacity(collection);
    uint32_t head = Collection_head(collection);
    uint8_t *collectionBuffer = Collection_dataBuffer(collection);
    bool reportExhaustion = Collection_reportExhaustion(collection, 16u);
    uint64_t exhaustionCount = Collection_exhaustionCount(collection);
    Collection_resetExhaustion(collection);
    uint64_t readSlot = Collection_readSlot(collection, 0u);
    Collection_writeSlot(collection, 0u, 42u);
    uint64_t readSlotUnsafe = Collection_readSlotUnsafe(collection, 0u);
    Collection_writeSlotUnsafe(collection, 0u, 42u);
    Array_free(array);
    return 0;
}
```

## Deque class (deque.c)

```c
#include "oop/type.h"
#include "struct/deque.h"

int main(void)
{
    Deque *deque = Deque(ID_INT, 4u);
    Deque_addFirst(deque, 1u);
    Deque_addLast(deque, 2u);
    uint64_t removeFirst = Deque_removeFirst(deque);
    uint64_t removeLast = Deque_removeLast(deque);
    uint64_t peekFirst = Deque_peekFirst(deque);
    uint64_t peekLast = Deque_peekLast(deque);
    uint64_t firstValue = Deque_get(deque, 0u);
    uint8_t *firstSlot = Deque_slot(deque, 0u);
    bool isEmpty = Deque_isEmpty(deque);
    size_t itemCount = Deque_size(deque);
    uint64_t exhaustionCount = Deque_exhaustionCount(deque);
    size_t itemLength = Deque_length(deque);
    size_t itemCapacity = Deque_capacity(deque);
    uint32_t elementClassId = Deque_elementClassId(deque);
    size_t stride = Deque_stride(deque);
    size_t head = Deque_head(deque);
    uint8_t *dequeBuffer = Deque_dataBuffer(deque);
    Deque_free(deque);
    return 0;
}
```

## CircleArray class (circle_array.c)

`CircleArray_getGrid` and `CircleArray_getOffset` still fill caller-provided
destinations; they are migration gaps under the Value Return Law.
`CircleArray_forEach` requires a callback, so callback-driven traversal is
also left as a documented gap.

```c
#include "oop/type.h"
#include "struct/circle_array.h"

int main(void)
{
    CircleArray *circle = CircleArray(2, ID_INT);
    uint64_t cellValue = 42u;
    int32_t radius = CircleArray_radius(circle);
    int32_t diameter = CircleArray_diameter(circle);
    size_t validCellCount = CircleArray_validCellCount(circle);
    bool containsGrid = CircleArray_containsGrid(circle, 2, 2);
    bool containsOffset = CircleArray_containsOffset(circle, 0, 0);
    int64_t distanceSquaredGrid = CircleArray_distanceSquaredGrid(circle, 2, 2);
    int64_t distanceSquaredOffset = CircleArray_distanceSquaredOffset(0, 0);
    bool gridSet = CircleArray_setGrid(circle, 2, 2, &cellValue);
    bool offsetSet = CircleArray_setOffset(circle, 0, 0, &cellValue);
    uint8_t *gridSlot = CircleArray_slotGrid(circle, 2, 2);
    uint8_t *offsetSlot = CircleArray_slotOffset(circle, 0, 0);
    CircleArray_free(circle);
    return 0;
}
```

## List class (list.c)

```c
#include "oop/type.h"
#include "struct/list.h"

int main(void)
{
    List *list = List(ID_INT, 4u);
    List *other = List(ID_INT, 4u);
    List_add(list, 42u);
    uint8_t *newSlot = List_addSlot(list);
    uint64_t firstValue = List_get(list, 0u);
    List_set(list, 0u, 84u);
    uint8_t *firstSlot = List_slot(list, 0u);
    List_remove(list, 1u);
    bool compare = List_compare(list, other);
    bool isEmpty = List_isEmpty(list);
    size_t itemCount = List_size(list);
    uint64_t exhaustionCount = List_exhaustionCount(list);
    size_t itemLength = List_length(list);
    size_t itemCapacity = List_capacity(list);
    uint32_t elementClassId = List_elementClassId(list);
    size_t stride = List_stride(list);
    uint8_t *listBuffer = List_dataBuffer(list);
    List_free(other);
    List_free(list);
    return 0;
}
```

## Queue class (queue.c)

```c
#include "oop/type.h"
#include "struct/queue.h"

int main(void)
{
    Queue *queue = Queue(ID_INT, 4u);
    Queue_push(queue, 42u);
    uint64_t pop = Queue_pop(queue);
    uint64_t peek = Queue_peek(queue);
    uint8_t *firstSlot = Queue_slot(queue, 0u);
    bool isEmpty = Queue_isEmpty(queue);
    size_t itemCount = Queue_size(queue);
    uint64_t exhaustionCount = Queue_exhaustionCount(queue);
    size_t itemLength = Queue_length(queue);
    size_t itemCapacity = Queue_capacity(queue);
    uint32_t elementClassId = Queue_elementClassId(queue);
    size_t stride = Queue_stride(queue);
    size_t head = Queue_head(queue);
    uint8_t *queueBuffer = Queue_dataBuffer(queue);
    Queue_free(queue);
    return 0;
}
```

## Stack class (stack.c)

```c
#include "oop/type.h"
#include "struct/stack.h"

int main(void)
{
    Stack *stack = Stack(ID_INT, 4u);
    Stack_push(stack, 42u);
    TryValue pushTry = Stack_pushTry(stack, 84u);
    uint64_t pop = Stack_pop(stack);
    uint64_t peek = Stack_peek(stack);
    uint8_t *firstSlot = Stack_slot(stack, 0u);
    bool isEmpty = Stack_isEmpty(stack);
    size_t itemCount = Stack_size(stack);
    uint64_t exhaustionCount = Stack_exhaustionCount(stack);
    size_t itemLength = Stack_length(stack);
    size_t itemCapacity = Stack_capacity(stack);
    uint32_t elementClassId = Stack_elementClassId(stack);
    size_t stride = Stack_stride(stack);
    uint8_t *stackBuffer = Stack_dataBuffer(stack);
    Stack_free(stack);
    return 0;
}
```

## Map class (map.c)

```c
#include "oop/type.h"
#include "struct/map.h"

int main(void)
{
    Map *map = Map(ID_INT, ID_INT, 16u);
    Map_put(map, 1u, 42u);
    uint64_t mappedValue = Map_get(map, 1u);
    bool containsKey = Map_containsKey(map, 1u);
    uint64_t remove = Map_remove(map, 1u);
    Array *keys = Map_keys(map);
    bool isEmpty = Map_isEmpty(map);
    size_t entryCount = Map_size(map);
    uint64_t exhaustionCount = Map_exhaustionCount(map);
    size_t mapCapacity = Map_capacity(map);
    uint32_t keyClassId = Map_keyClassId(map);
    uint32_t valClassId = Map_valClassId(map);
    uint8_t *mapBuffer = Map_dataBuffer(map);
    Array_free(keys);
    Map_free(map);
    return 0;
}
```

## Set class (set.c)

```c
#include "oop/type.h"
#include "struct/set.h"

int main(void)
{
    Set *set = Set(ID_INT, 16u);
    int add = Set_add(set, 42u);
    bool containsValue = Set_contains(set, 42u);
    int remove = Set_remove(set, 42u);
    List *values = Set_toList(set);
    List_free(values);
    List *sortedValues = Set_toSortedList(set);
    List_free(sortedValues);
    bool isEmpty = Set_isEmpty(set);
    size_t valueCount = Set_size(set);
    uint64_t exhaustionCount = Set_exhaustionCount(set);
    size_t setCapacity = Set_capacity(set);
    uint32_t elementClassId = Set_elementClassId(set);
    uint8_t *setBuffer = Set_dataBuffer(set);
    Set_free(set);
    return 0;
}
```

## MinHeap class (minheap.c)

`MinHeap` has no zero-argument constructor arm in the cookbook; construct it
with a capacity through the class macro.

```c
#include "struct/minheap.h"

int main(void)
{
    MinHeap *heap = MinHeap(16u);
    size_t heapSize = MinHeap_size(heap);
    size_t heapCapacity = MinHeap_capacity(heap);
    bool isEmpty = MinHeap_isEmpty(heap);
    uint64_t exhaustionCount = MinHeap_exhaustionCount(heap);
    int push = MinHeap_push(heap, 42, 0.5f);
    int32_t poppedItem = MinHeap_popItem(heap);
    int32_t nextItem = MinHeap_peekItem(heap);
    MinHeap_free(heap);
    return 0;
}
```

## SparseSet class (sparseset.c)

```c
#include "struct/sparseset.h"

int main(void)
{
    SparseSet *set = SparseSet(16u, 128u, sizeof(uint64_t));
    size_t entityCount = SparseSet_count(set);
    uint64_t exhaustionCount = SparseSet_exhaustionCount(set);
    size_t capacity = SparseSet_capacity(set);
    size_t maxEntities = SparseSet_maxEntities(set);
    bool containsEntity = SparseSet_contains(set, 7);
    uint8_t *addedEntity = SparseSet_add(set, 7);
    SparseSet_remove(set, 7);
    uint8_t *entityData = SparseSet_get(set, 7);
    const int32_t *denseEntities = SparseSet_denseEntities(set);
    const uint8_t *denseData = SparseSet_denseData(set);
    SparseSet_free(set);
    return 0;
}
```

## SphereArray class (sphere_array.c)

`SphereArray_getGrid` and `SphereArray_getOffset` still fill caller-provided
destinations; they are migration gaps under the Value Return Law.
`SphereArray_forEach` requires a callback, so callback-driven traversal is
also left as a documented gap.

```c
#include "oop/type.h"
#include "struct/sphere_array.h"

int main(void)
{
    SphereArray *sphere = SphereArray(2, ID_INT);
    uint64_t voxelValue = 42u;
    int32_t radius = SphereArray_radius(sphere);
    int32_t diameter = SphereArray_diameter(sphere);
    size_t validVoxelCount = SphereArray_validVoxelCount(sphere);
    bool containsGrid = SphereArray_containsGrid(sphere, 2, 2, 2);
    bool containsOffset = SphereArray_containsOffset(sphere, 0, 0, 0);
    int64_t distanceSquaredGrid = SphereArray_distanceSquaredGrid(sphere, 2, 2, 2);
    int64_t distanceSquaredOffset = SphereArray_distanceSquaredOffset(0, 0, 0);
    bool gridSet = SphereArray_setGrid(sphere, 2, 2, 2, &voxelValue);
    bool offsetSet = SphereArray_setOffset(sphere, 0, 0, 0, &voxelValue);
    uint8_t *gridSlot = SphereArray_slotGrid(sphere, 2, 2, 2);
    uint8_t *offsetSlot = SphereArray_slotOffset(sphere, 0, 0, 0);
    SphereArray_free(sphere);
    return 0;
}
```

## StructExhaustion functions (exhaustion.c)

This utility module has no owned object or constructor macro. Its functions
operate on the owning object's refusal counter and report latch.

```c
#include "struct/exhaustion.h"

int main(void)
{
    uint64_t refusalCount = 0u;
    bool refusalReported = false;
    bool reported = Struct_reportExhaustion(&refusalCount, &refusalReported,
        "owner-name-goes-here", 64u, 32u);
    uint64_t exhaustionCount = Struct_exhaustionCount(&refusalCount);
    Struct_resetExhaustion(&refusalCount, &refusalReported);
    bool reportConstructionExhaustion = Struct_reportConstructionExhaustion("owner-name-goes-here", 64u);
    uint64_t constructionExhaustionCount = Struct_constructionExhaustionCount();
    Struct_resetConstructionExhaustion();
    return 0;
}
```

## Equals functions (equals.c)

This utility module has no owned object or constructor macro.

```c
#include "c23/equals.h"

int main(void)
{
    bool valuesEqual = isEqual(nullptr, nullptr);
    bool namesMatch = isEquallyNamed(nullptr, "first-name-goes-here", "second-name-goes-here");
    return 0;
}
```

## Destructor functions (free.c)

The custom destructor callback cannot be demonstrated under the one-main,
no-helper cookbook format. Registration and lookup need a real callback, so
`Destructor_register` and `Destructor_lookup` remain explicit callback gaps.

```c
#include "c23/free.h"

int main(void)
{
    c23_free(nullptr);
    return 0;
}
```

## Stride functions (stride.c)

This utility module has no owned object or constructor macro.

```c
#include "oop/stride.h"
#include "oop/type.h"

int main(void)
{
    size_t integerStride = Stride_get(ID_INT);
    return 0;
}
```

## Str class (lang/str.c)

`Str(...)` currently binds a caller-provided destination buffer, which
conflicts with the Value Return Law. `Str_put`, `Str_putc`, `Str_putQuoted`,
and `Str_printf` write into that buffer; `Str_isTruncated`, `Str_length`, and
`Str_cstr` require the resulting builder instance. All remain blocked until the
builder has a destination-free constructor and value-returning operations.

```c
int main(void)
{
    return 0;
}
```

## GestureState class (gesture.c)

```c
#include "input/gesture.h"

int main(void)
{
    GestureState state = GestureState();
    GestureEvent event = GestureEvent(GESTURE_PHASE_CHANGED, 0.1f);
    GestureState_processEvent(&state, event);
    GestureState_tick(&state, 0.016f);
    return 0;
}
```

## GestureEvent class (gesture.h)

```c
#include "input/gesture.h"

int main(void)
{
    GestureEvent event = GestureEvent(GESTURE_PHASE_CHANGED, 0.1f);
    GestureEvent_setPhase(&event, GESTURE_PHASE_ENDED);
    GestureEvent_setMagnificationDelta(&event, 0.2f);
    return 0;
}
```

## HardwareEvent class (hardware_event.c)

This file has no `HardwareEvent(...)` constructor macro. Its public
`HardwareEvent_makeGamepad`, `HardwareEvent_makeGesture`,
`HardwareEvent_makePiano`, and `HardwareEvent_makeTurntable` functions are
constructor factories and remain an API ergonomics gap; the cookbook does not
present those factory spellings as the preferred way to construct an event.

```c
#include "input/hardware_event.h"

int main(void)
{
    return 0;
}
```

## PianoKey functions (piano_key.c)

`PianoKey_noteName` still writes into a caller-provided buffer, so it remains a
Value Return Law migration gap. Other value-returning operations are shown.

```c
#include "input/piano_key.h"

int main(void)
{
    float noteFrequency = PianoKey_frequency(69u);
    float equalTemperamentFrequency = PianoKey_equal_temperament_hz(69u);
    PianoPitchClass pitchClass = PianoKey_pitchClass(69u);
    int32_t octave = PianoKey_octave(69u);
    PianoState state = PianoState();
    PianoKeyEvent event = PianoKeyEvent(60u, true, 0.8f);
    PianoState_processEvent(&state, event);
    bool isNoteOn = PianoState_isNoteOn(&state, 60u);
    float noteVelocity = PianoState_noteVelocity(&state, 60u);
    return 0;
}
```

## PianoKeyEvent class (piano_key.h)

```c
#include "input/piano_key.h"

int main(void)
{
    PianoKeyEvent event = PianoKeyEvent(60u, true, 0.8f);
    PianoKeyEvent_setNote(&event, 61u);
    PianoKeyEvent_setDown(&event, false);
    PianoKeyEvent_setVelocity(&event, 0.6f);
    return 0;
}
```

## Loop class (loop.c)

The loop requires a non-null tick callback to run. `Loop_setTick` and
`Loop_run` therefore remain callback gaps because this one-main format cannot
define the required callback.

```c
#include "engine/loop.h"

int main(void)
{
    Loop loop = Loop(nullptr, nullptr, 16);
    Loop_setUserdata(&loop, nullptr);
    Loop_setFrameMilliseconds(&loop, 16);
    Loop_stop(&loop);
    return 0;
}
```

## Exception class (exception.c)

`Exception_setDetailsV` needs a valid `va_list`, which cannot be started in
this standalone non-variadic `main()` without a helper function. The string
projections are caller-buffer APIs and remain Value Return Law gaps.

```c
#include "exception/exception.h"

int main(void)
{
    Exception exception = Exception(EXCEPTION_IO, "operation-name-goes-here",
        "source-file-goes-here", 42, "reason-goes-here: %s", "detail-goes-here");
    Exception_setDetails(&exception, "context-goes-here: %d", 7);
    const char *categoryName = Exception_categoryName(EXCEPTION_IO);
    Exception_print(&exception);
    Exception_free(&exception);
    return 0;
}
```

## TryPtr class (try_ptr.c)

`TryPtr_toString` and `TryPtr_toStringStruct` require caller-provided output
buffers and remain migration gaps under the Value Return Law. The constructor
example uses `TryPtr(...)`; it does not call the factory arms directly.
`TryPtr_ok` and `TryPtr_error` are named success/error factories with no
corresponding macro forms and remain constructor ergonomics gaps.

```c
#include "exception/try_ptr.h"

int main(void)
{
    int value = 42;
    TryPtr result = TryPtr(&value, TRY_OK);
    void *pointerValue = TryPtr_getValue(&result);
    TryPtr_setValue(&result, &value);
    TryCode pointerCode = TryPtr_getCode(&result);
    TryPtr_setCode(&result, TRY_OK);
    bool pointerIsOk = TryPtr_isOk(&result);
    return 0;
}
```

## TryValue class (try_value.c)

`TryValue_toString` and `TryValue_toStringStruct` require caller-provided
output buffers and remain migration gaps under the Value Return Law. The
constructor example uses `TryValue(...)`; it does not call the factory arms
directly. `TryValue_ok` and `TryValue_error` are named success/error factories
with no corresponding macro forms and remain constructor ergonomics gaps.

```c
#include "exception/try_value.h"

int main(void)
{
    TryValue result = TryValue(42u, TRY_OK);
    uint64_t resultValue = TryValue_getValue(&result);
    TryValue_setValue(&result, 84u);
    TryCode resultCode = TryValue_getCode(&result);
    TryValue_setCode(&result, TRY_OK);
    bool isOk = TryValue_isOk(&result);
    return 0;
}
```

## Png functions (png.c)

`Png_decode` and `Png_decodeMalloc` write pixel buffers and image dimensions
through caller-provided output parameters; they remain Value Return Law
migration gaps. The signature and status-name operations return values
directly.

```c
#include "image/png.h"

int main(void)
{
    const uint8_t *pngBytes = nullptr;
    bool isPng = Png_isPng(pngBytes, 0u);
    const char *codeName = Png_codeName(PNG_INVALID);
    return 0;
}
```

## ReactiveObject family (reactive_object.c)

This source stamps seven typed classes. Each constructor, setter, getter, and
free call is shown. The `*_addOnSet`, `*_removeOnSet`, `*_addOnChanged`,
`*_removeOnChanged`, `*_addOnGet`, `*_removeOnGet`, `*_addOnNullptr`, and
`*_removeOnNullptr` APIs require real callbacks, which a one-main example
cannot define; those observer calls remain callback gaps.

```c
#include "reactive/reactive_object.h"

int main(void)
{
    Vec2 *vec2Initial = Vec2(1.0f, 2.0f);
    Vec2 *vec2Updated = Vec2(3.0f, 4.0f);
    ReactiveVec2 *vec2 = ReactiveVec2(vec2Initial);
    ReactiveVec2_set(vec2, vec2Updated);
    Vec2 *vec2Value = ReactiveVec2_get(vec2);
    ReactiveVec2_free(vec2);
    Vec2_free(vec2Updated);
    Vec2_free(vec2Initial);

    Vec3 *vec3Initial = Vec3(1.0f, 2.0f, 3.0f);
    Vec3 *vec3Updated = Vec3(4.0f, 5.0f, 6.0f);
    ReactiveVec3 *vec3 = ReactiveVec3(vec3Initial);
    ReactiveVec3_set(vec3, vec3Updated);
    Vec3 *vec3Value = ReactiveVec3_get(vec3);
    ReactiveVec3_free(vec3);
    Vec3_free(vec3Updated);
    Vec3_free(vec3Initial);

    Vec4 *vec4Initial = Vec4(1.0f, 2.0f, 3.0f, 1.0f);
    Vec4 *vec4Updated = Vec4(4.0f, 5.0f, 6.0f, 1.0f);
    ReactiveVec4 *vec4 = ReactiveVec4(vec4Initial);
    ReactiveVec4_set(vec4, vec4Updated);
    Vec4 *vec4Value = ReactiveVec4_get(vec4);
    ReactiveVec4_free(vec4);
    Vec4_free(vec4Updated);
    Vec4_free(vec4Initial);

    Rectangle *rectangleInitial = Rectangle(0.0f, 0.0f, 100.0f, 80.0f);
    Rectangle *rectangleUpdated = Rectangle(10.0f, 20.0f, 120.0f, 90.0f);
    ReactiveRectangle *rectangle = ReactiveRectangle(rectangleInitial);
    ReactiveRectangle_set(rectangle, rectangleUpdated);
    Rectangle *rectangleValue = ReactiveRectangle_get(rectangle);
    ReactiveRectangle_free(rectangle);
    Rectangle_free(rectangleUpdated);
    Rectangle_free(rectangleInitial);

    IntDouble *intDoubleInitial = IntDouble(7, 0.5);
    IntDouble *intDoubleUpdated = IntDouble(9, 0.75);
    ReactiveIntDouble *intDouble = ReactiveIntDouble(intDoubleInitial);
    ReactiveIntDouble_set(intDouble, intDoubleUpdated);
    IntDouble *intDoubleValue = ReactiveIntDouble_get(intDouble);
    ReactiveIntDouble_free(intDouble);
    IntDouble_free(intDoubleUpdated);
    IntDouble_free(intDoubleInitial);

    LongFloat *longFloatInitial = LongFloat(7000LL, 0.25f);
    LongFloat *longFloatUpdated = LongFloat(8000LL, 0.5f);
    ReactiveLongFloat *longFloat = ReactiveLongFloat(longFloatInitial);
    ReactiveLongFloat_set(longFloat, longFloatUpdated);
    LongFloat *longFloatValue = ReactiveLongFloat_get(longFloat);
    ReactiveLongFloat_free(longFloat);
    LongFloat_free(longFloatUpdated);
    LongFloat_free(longFloatInitial);

    LongDouble *longDoubleInitial = LongDouble(9000LL, 0.125);
    LongDouble *longDoubleUpdated = LongDouble(10000LL, 0.25);
    ReactiveLongDouble *longDouble = ReactiveLongDouble(longDoubleInitial);
    ReactiveLongDouble_set(longDouble, longDoubleUpdated);
    LongDouble *longDoubleValue = ReactiveLongDouble_get(longDouble);
    ReactiveLongDouble_free(longDouble);
    LongDouble_free(longDoubleUpdated);
    LongDouble_free(longDoubleInitial);
    return 0;
}
```

## ReactiveProbableInt class (reactive_probable.c)

The `ReactiveProbableInt_addOn*` and `ReactiveProbableInt_removeOn*` observer
APIs require real callbacks, which a one-main example cannot define; those
observer calls remain callback gaps.

```c
#include "reactive/reactive_probable.h"

int main(void)
{
    ReactiveProbableInt *value = ReactiveProbableInt(42, 0.75f);
    ReactiveProbableInt_set(value, 84, 0.5f);
    int32_t probableValue = ReactiveProbableInt_get(value);
    float chance = ReactiveProbableInt_getChance(value);
    ReactiveProbableInt_free(value);
    return 0;
}
```

## Bespoke class (bespoke.c)

```c
#include "spoke/bespoke.h"

int main(void)
{
    Bespoke *bridge = Bespoke();
    bridgeBespoke();
    bool driversChanged = bridgeBespokeCheck();
    BespokeState graphicsState = bridgeBespokeGraphicsState();
    BespokeState networkingState = bridgeBespokeNetworkingState();
    BespokeState otherState = bridgeBespokeSmthState();
    Bespoke_bridge(bridge);
    bool localCheckChanged = Bespoke_check(bridge);
    return 0;
}
```

## Audio backend functions (audio_cocoa.m)

This section refers to the Cocoa backend, but `audio_cocoa.m` is absent from
this checkout; only `audio_stub.c` and the HAL stub exist. The header declares
the shared audio API, but there is no Cocoa implementation to inspect or
demonstrate. The section below is therefore an API-level call example only,
not evidence of a working Cocoa backend. `AudioClip` still has no preferred
`AudioClip(...)` constructor macro; its factory calls are direct API calls.

```c
#include "audio/audio.h"

int main(void)
{
    bool audioReady = Audio_isReady();
    AudioVoice *voice = AudioVoice();
    AudioVoice_setClip(voice, nullptr);
    AudioVoice_setGain(voice, 0.8f);
    AudioVoice_setPitch(voice, 1.0f);
    AudioVoice_setLooping(voice, false);
    AudioVoice_play(voice);
    AudioVoice_pause(voice);
    AudioVoice_stop(voice);
    bool voiceIsPlaying = AudioVoice_isPlaying(voice);
    AudioVoice_free(voice);
    Audio *audio = Audio(48000.0, AUDIO_STEREO);
    Audio *defaultAudio = Audio();
    Audio *pathAudio = Audio("audio-file-path-goes-here");
    Audio *numericAudio = Audio(44100.0);
    Audio_setGain(audio, 0.8f);
    float gain = Audio_getGain(audio);
    Audio_setPitch(audio, 1.0f);
    float pitch = Audio_getPitch(audio);
    Audio_setLooping(audio, false);
    bool looping = Audio_getLooping(audio);
    Audio_setSampleRate(audio, 48000.0);
    double sampleRate = Audio_getSampleRate(audio);
    Audio_setChannels(audio, AUDIO_STEREO);
    int channels = Audio_getChannels(audio);
    Audio_play(audio);
    Audio_pause(audio);
    Audio_stop(audio);
    bool isPlaying = Audio_isPlaying(audio);
    Audio_free(audio);
    Audio_free(defaultAudio);
    Audio_free(pathAudio);
    Audio_free(numericAudio);
    Audio_shutdown();
    return 0;
}
```

## AudioHal backend functions (audio_hal_mac.m)

The HAL renders silence when the callback is null. A useful real-time render
callback cannot be shown under the one-main, no-helper example rule.

```c
#include "audio/audio_hal.h"

int main(void)
{
    AudioHalConfig config = AudioHalConfig(nullptr, nullptr);
    AudioHalConfig defaults = AudioHalConfig();
    AudioHalConfig callbackConfig = AudioHalConfig(nullptr);
    bool configSampleRateSet = AudioHalConfig_set_sample_rate(&config, 48000.0);
    bool channels = AudioHalConfig_set_channels(&config, 2u);
    bool frames = AudioHalConfig_set_buffer_frames(&config, 256u);
    bool defaultsSampleRateSet = AudioHalConfig_set_sample_rate(&defaults, 44100.0);
    bool channels2 = AudioHalConfig_set_channels(&defaults, 2u);
    bool frames2 = AudioHalConfig_set_buffer_frames(&defaults, 128u);
    bool callbackSampleRateSet = AudioHalConfig_set_sample_rate(&callbackConfig, 48000.0);
    bool channels3 = AudioHalConfig_set_channels(&callbackConfig, 2u);
    bool frames3 = AudioHalConfig_set_buffer_frames(&callbackConfig, 128u);
    AudioHal *defaultHal = AudioHal();
    AudioHal *hal = AudioHal(&config);
    bool isStarted = AudioHal_start(hal);
    bool running = AudioHal_is_running(hal);
    double rate = AudioHal_get_sample_rate(hal);
    uint32_t channels4 = AudioHal_get_channels(hal);
    uint32_t frames4 = AudioHal_get_buffer_frames(hal);
    double ms = AudioHal_get_latency_ms(hal);
    bool stop = AudioHal_stop(hal);
    AudioHal_destroy(hal);
    AudioHal_destroy(defaultHal);
    return 0;
}
```

## SystemDiscovery class (objc/discovery.m)

```c
#include "system/discovery.h"

int main(void)
{
    SystemDiscovery_bootstrap();
    bool isBootstrapped = SystemDiscovery_isBootstrapped();
    SystemDiscovery_refresh();
    return 0;
}
```

## Legacy Apple TLS backend (objc/tls_apple.m)

This older duplicate exports `Tls_connect`, `Tls_send`, `Tls_recv`, and
`Tls_close`. It has no `TlsConn(...)` constructor macro, while connect and
receive require caller-provided destinations, so those calls remain migration
gaps. The active Vexspoke TLS seam is implemented by `net/tls_apple.m`.

```c
#include "net/tls.h"

int main(void)
{
    bool sent = Tls_send(nullptr, "request-bytes-goes-here", 23u);
    Tls_close(nullptr);
    return 0;
}
```

## TouchID functions (touchid_cocoa.m)

```c
#include "security/touchid.h"

int main(void)
{
    TouchIDToken token = TouchID_authenticate("authorize-operation-goes-here");
    bool verify = TouchID_verify(token);
    TouchID_discard(token);
    return 0;
}
```

## VariableSlot class (variable_slot.c)

`VariableSlot(...)` allocates the object and applies its name and pointer
internally; callers use the constructor macro shown below rather than the
lower-level initializer.
`VariableSlot_foldName` writes the folded name through an output buffer, while
`VariableSlot_toString` and `VariableSlot_toStringStruct` write projections to
caller-provided destinations. These APIs remain Value Return Law migration
gaps. `VariableSlot_init` is the lower-level initializer already used by
`VariableSlot()`; the example uses the preferred macro.

```c
#include "relational/variable_slot.h"

int main(void)
{
    VariableSlot *slot = VariableSlot("variable-name-goes-here",
        (uintptr_t) 42u);
    int bucketOf = VariableSlot_bucketOf('v');
    bool nameSet = VariableSlot_setName(slot, "renamed-variable-goes-here");
    VariableSlot_setPointer(slot, (uintptr_t) 84u);
    const char *name = VariableSlot_getName(slot);
    uintptr_t pointer = VariableSlot_getPointer(slot);
    bool isEmpty = VariableSlot_isEmpty(slot);
    bool nameEquals = VariableSlot_nameEquals(slot, "renamed-variable-goes-here");


    VariableSlot_free(slot);
    return 0;
}
```

## VariableMiniMap class (variable_mini_map.c)

`VariableMiniMap()` allocates and initializes the map internally; callers use
the constructor macro shown below rather than the lower-level initializer.
`VariableMiniMap_toString` and `VariableMiniMap_toStringStruct` require
caller-provided buffers, so they remain migration gaps. The callback API
`VariableMiniMap_forEach` requires a visitor implementation and is not
illustrated here. `VariableMiniMap_init` and `VariableMiniMap_shutdown` are
lower-level lifecycle calls handled by the preferred constructor and free
operation.

```c
#include "relational/variable_mini_map.h"

int main(void)
{
    VariableMiniMap *map = VariableMiniMap();
    bool add = VariableMiniMap_add(map, "variable-name-goes-here", (uintptr_t) 42u);
    uintptr_t pointer = VariableMiniMap_get(map, "variable-name-goes-here");
    bool contains = VariableMiniMap_contains(map, "variable-name-goes-here");
    uint32_t count = VariableMiniMap_count(map);
    bool isEmpty = VariableMiniMap_isEmpty(map);

    VariableMiniMap_free(map);
    return 0;
}
```

## VariableHashMap class (variable_hash_map.c)

`VariableHashMap()` allocates and initializes the map internally; callers use
the constructor macro shown below rather than the lower-level initializer.
`VariableHashMap_toString` and `VariableHashMap_toStringStruct` require
caller-provided buffers, so they remain migration gaps. The callback API
`VariableHashMap_forEach` requires a visitor implementation and is not
illustrated here. `VariableHashMap_init` and `VariableHashMap_shutdown` are
lower-level lifecycle calls handled by the preferred constructor and free
operation.

```c
#include "relational/variable_hash_map.h"

int main(void)
{
    VariableHashMap *map = VariableHashMap();
    bool add = VariableHashMap_add(map, "variable-name-goes-here", (uintptr_t) 42u);
    uintptr_t pointer = VariableHashMap_get(map, "variable-name-goes-here");
    bool contains = VariableHashMap_contains(map, "variable-name-goes-here");
    uint32_t count = VariableHashMap_count(map);
    bool isEmpty = VariableHashMap_isEmpty(map);

    VariableHashMap_free(map);
    return 0;
}
```

## StringPool class (variable_pool.c)

`StringPool` has no `StringPool(...)` constructor macro and requires the
`StringPool_init()` lifecycle call with a live `MemoryArena`. The engine has no
`MemoryArena(...)` macro either, so its create/init sequence is an explicit
constructor and lifecycle gap. Only `StringPool_count()` safely returns a
meaningful value before initialization; `StringPool_shutdown()` is safe and
idempotent before initialization, so both direct calls are shown. The
`StringPool_intern`, `StringPool_find`, `StringPool_slot`, `StringPool_name`,
and `StringPool_isSlot` operations remain blocked on initialization.

```c
#include "relational/variable_pool.h"

int main(void)
{
    uint32_t slotCount = StringPool_count();
    StringPool_shutdown();
    return 0;
}
```

## ChunkedList class (chunked_list.c)

`ChunkedList_packInto` still requires a caller buffer, and
`ChunkedList_forEachChunk` needs a callback function that a one-main call
example cannot define. Those are API migration gaps under the value-return
and cookbook rules. `ChunkedList_paged` is reached through the public
`ChunkedList(...)` constructor macro and is not called directly.

```c
#include "struct/chunked_list.h"
#include "oop/type.h"

int main(void)
{
    ChunkedList *list = ChunkedList(ID_INT, sizeof(uint64_t), CHUNKED_LIST_TWO_LAYER_DEFAULT);
    ChunkedList_setChunkBytes(list, 256u);
    uint8_t *row = ChunkedList_addSlot(list);
    bool reserve = ChunkedList_reserve(list, 32u);
    uint8_t *firstRow = ChunkedList_slot(list, 0u);
    uint8_t *firstChunk = ChunkedList_getChunk(list, 0u);
    uint8_t *nextChunk = ChunkedList_nextChunk(list, firstChunk);
    uint32_t size = ChunkedList_size(list);
    uint32_t length = ChunkedList_length(list);
    uint32_t capacity = ChunkedList_capacity(list);
    bool isEmpty = ChunkedList_isEmpty(list);
    uint64_t exhaustionCount = ChunkedList_exhaustionCount(list);
    uint32_t elementClassId = ChunkedList_elementClassId(list);
    uint32_t stride = ChunkedList_stride(list);
    uint32_t chunkCount = ChunkedList_getChunkCount(list);
    uint32_t rowsPerChunk = ChunkedList_getRowsPerChunk(list);
    uint32_t chunkBytes = ChunkedList_getChunkBytes(list);
    uint32_t levels = ChunkedList_getLevels(list);


    ChunkedList_free(list);
    return 0;
}
```

## Octree class (octree.c)

The two query functions currently write results into caller-provided payload
buffers; they are documented migration gaps and are not called here.

```c
#include "struct/octree.h"

int main(void)
{
    OctreeAABB bounds = OctreeAABB(-10.0f, -10.0f, -10.0f, 10.0f, 10.0f, 10.0f);
    OctreeAABB_setMin(&bounds, -12.0f, -12.0f, -12.0f);
    OctreeAABB_setMax(&bounds, 12.0f, 12.0f, 12.0f);
    OctreePoint point = OctreePoint(1.0f, 2.0f, 3.0f);
    OctreePoint_set(&point, 2.0f, 3.0f, 4.0f);
    bool containsPoint = OctreeAABB_containsPoint(bounds, point);
    bool intersects = OctreeAABB_intersects(bounds, bounds);
    bool intersectsSphere = OctreeAABB_intersectsSphere(bounds, point, 2.0f);
    Octree *tree = Octree(bounds, 8u, 8u);
    bool insert = Octree_insert(tree, point, 42u);
    size_t nodeCount = Octree_count(tree);
    uint64_t exhaustionCount = Octree_exhaustionCount(tree);
    Octree_clear(tree);
    Octree_free(tree);
    return 0;
}
```

## WebSocket class (websocket.c)

`WebSocket_open` needs a `WebSocketConfig`, but the public API has no
constructor/setters for that value record. `WebSocket_toString` and
`WebSocket_toStringStruct` require caller-provided destinations. Those APIs
remain documented migration gaps and are omitted from the call example.

```c
#include "net/websocket.h"

int main(void)
{
    WebSocket socket = WebSocket();
    WebSocketState state = WebSocket_state(&socket);
    bool isOpen = WebSocket_isOpen(&socket);
    const char *lastError = WebSocket_lastError(&socket);
    uint16_t closeCode = WebSocket_closeCode(&socket);
    const char *closeReason = WebSocket_closeReason(&socket);
    size_t maxMessageBytes = WebSocket_maxMessageBytes(&socket);
    uint64_t framesIn = WebSocket_framesIn(&socket);
    uint64_t framesOut = WebSocket_framesOut(&socket);
    uint64_t pongsSent = WebSocket_pongsSent(&socket);
    WebSocketMessage message = WebSocket_poll(&socket, 10u);
    bool textSent = WebSocket_writeText(&socket, "message-goes-here", 17u);
    const uint8_t *payload = (const uint8_t *) "binary-payload-goes-here";
    bool binarySent = WebSocket_writeBinary(&socket, payload, 24u);
    bool pingSent = WebSocket_writePing(&socket, payload, 4u);
    bool closeSent = WebSocket_writeClose(&socket, 1000u, "normal-close");
    WebSocket_close(&socket);
    return 0;
}
```

## VexWsSource class (vex_ws_source.c)

`VexWsSource_open` also needs the unavailable `WebSocketConfig` constructor or
setters. `VexWsSource_toString` and `VexWsSource_toStringStruct` require
caller-provided destinations. These remain documented migration gaps. The
seam operations are ordinary direct calls here; no callback definitions or
callback invocation is needed.

```c
#include "net/vex_ws_source.h"

int main(void)
{
    VexWsSource source = VexWsSource();
    bool connected = VexWsSource_connect(&source);
    uint32_t delivered = VexWsSource_poll(&source, 10u);
    const uint8_t *payload = (const uint8_t *) "message-goes-here";
    bool sent = VexWsSource_send(&source, payload, 18u);
    const WebSocketMessage *lastMessage = VexWsSource_last(&source);
    WebSocket *socket = VexWsSource_socket(&source);
    const char *url = VexWsSource_url(&source);
    bool isOpen = VexWsSource_isOpen(&source);
    VexWsSource_close(&source);
    return 0;
}
```
