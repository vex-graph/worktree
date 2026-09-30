/*
 * ============================================================================
 * pointer_translation_lab.c — The Interactive Java-to-C Pointer Translation Lab
 * ============================================================================
 * 
 * For the 'anti' engine developer transitioning from Java / FFM to pure C23.
 * 
 * Compile & Run:
 *   clang -std=c23 -Wall -Wextra -Werror -mcpu=native pointer_translation_lab.c -o pointer_lab  # portable across Apple Silicon; baseline apple-m1 if strict
 *   ./pointer_lab
 * 
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>
#include <assert.h>

// Helper to print section banners
static void print_banner(const char *title) {
    printf("\n====================================================================\n");
    printf(" %s\n", title);
    printf("====================================================================\n");
}

/* ============================================================================
 * MODULE 0: The Core Concept — Address vs Value
 * ----------------------------------------------------------------------------
 * JAVA:       int x = 42; (x lives on JVM stack; address is completely hidden)
 * JAVA FFM:   long addr = segment.address(); (raw 64-bit integer)
 * C23:        int x = 42;
 *             int *p = &x;     // '&' = Address-of operator (get location)
 *             int val = *p;    // '*' = Dereference operator (read/write value at location)
 * ============================================================================
 */
static void demo_module_0_basics(void) {
    print_banner("MODULE 0: Address (&) vs Dereference (*)");

    int value = 42;
    int *p = &value; // p stores the memory address of 'value'

    printf("[C Code]   int value = %d;\n", value);
    printf("[C Code]   int *p = &value;\n");
    printf("----------------------------------------------------\n");
    printf("1. Value directly:        value   = %d\n", value);
    printf("2. Address of value:      &value  = %p (hex address in RAM)\n", (void *)&value);
    printf("3. Pointer variable holds: p      = %p\n", (void *)p);
    printf("4. Address of pointer p:  &p      = %p (pointer itself lives in stack!)\n", (void *)&p);
    printf("5. Dereference pointer:   *p      = %d (reads the int at address p)\n", *p);

    // Writing through pointer
    *p = 99;
    printf("\n[Action] Executed: *p = 99;\n");
    printf("Result:  value is now %d (mutated through its address!)\n", value);
}

/* ============================================================================
 * MODULE 1: Java Reference vs C Pointer (Pass-by-Value vs Pass-by-Address)
 * ----------------------------------------------------------------------------
 * JAVA:
 *   void modify(int x) { x = 99; } // Does NOTHING to caller's x!
 *   void modify(MyObj o) { o.val = 99; } // Modifies object fields, but cannot repoint 'o'
 * 
 * C23:
 *   In C, EVERYTHING is strictly passed by value (copied).
 *   To let a function modify a caller's variable, pass the ADDRESS (a pointer)!
 * ============================================================================
 */
static void cannot_modify(int x) {
    x = 999; // Only modifies local copy on the stack
    (void)x; // Silence unused warning while illustrating that caller's copy is unaffected
}

static void can_modify(int *p) {
    *p = 999; // Dereferences caller's address and mutates caller's memory!
}

static void demo_module_1_pass_by_address(void) {
    print_banner("MODULE 1: Java Pass-by-Value vs C Pass-by-Address");

    int my_num = 10;
    printf("Initial my_num = %d\n", my_num);

    cannot_modify(my_num);
    printf("After cannot_modify(my_num):     my_num = %d (UNCHANGED, passed copy)\n", my_num);

    can_modify(&my_num);
    printf("After can_modify(&my_num):       my_num = %d (MUTATED via pointer!)\n", my_num);
}

/* ============================================================================
 * MODULE 2: Pointer Arithmetic (The "Stride" Rule)
 * ----------------------------------------------------------------------------
 * CRITICAL RULE:
 *   When you add 1 to a pointer (p + 1), it does NOT add 1 byte!
 *   It advances by: 1 * sizeof(*p) bytes!
 * 
 * JAVA EQUIVALENT:
 *   Java FFM / Unsafe: long elementAddr = baseAddr + (index * 4L); // manual int stride
 *   C23:               int *element = base_ptr + index;           // compiler scales automatically!
 * ============================================================================
 */
static void demo_module_2_pointer_arithmetic(void) {
    print_banner("MODULE 2: Pointer Arithmetic & Type Strides");

    int32_t int_array[4] = {100, 200, 300, 400};
    int32_t *p_int = int_array;

    printf("int32_t array base address: %p\n", (void *)p_int);
    for (int i = 0; i < 4; i++) {
        int32_t *elem_ptr = p_int + i;
        uintptr_t byte_diff = (uintptr_t)elem_ptr - (uintptr_t)p_int;
        printf("  index %d: p_int + %d = %p (offset: +%lu bytes) -> value = %d\n",
               i, i, (void *)elem_ptr, (unsigned long)byte_diff, *elem_ptr);
    }

    printf("\nNote: sizeof(int32_t) = %zu bytes. Each p_int + 1 jumps 4 bytes in RAM.\n", sizeof(int32_t));

    // Array indexing syntax is literally sugar for pointer arithmetic:
    // arr[i] == *(arr + i) == *(i + arr) == i[arr]
    printf("\nSyntactic Equivalence Proof:\n");
    printf("  int_array[2]   = %d\n", int_array[2]);
    printf("  *(p_int + 2)   = %d\n", *(p_int + 2));
    printf("  *(int_array+2) = %d\n", *(int_array + 2));
}

/* ============================================================================
 * MODULE 3: Structs & Pointers (The Arrow '->' Operator)
 * ----------------------------------------------------------------------------
 * JAVA:
 *   class Entity { int id; float x, y; }
 *   Entity e = new Entity();
 *   e.x = 10.0f;
 * 
 * C23:
 *   typedef struct { int32_t id; float x; float y; } Entity;
 *   Entity e = { .id = 1, .x = 10.0f, .y = 20.0f };
 *   Entity *ep = &e;
 *   ep->x = 15.0f;        // 'ep->x' is shorthand for '(*ep).x'
 * ============================================================================
 */
typedef struct Entity {
    int32_t id;
    float x;
    float y;
    uint32_t flags;
} Entity;

static void demo_module_3_struct_pointers(void) {
    print_banner("MODULE 3: Struct Pointers & Arrow Syntax (->)");

    Entity ent = { .id = 101, .x = 1.5f, .y = 3.5f, .flags = 0x01 };
    Entity *ptr = &ent;

    printf("Struct located at:       %p\n", (void *)ptr);
    printf("Field ent.id:            %d\n", ent.id);
    printf("Via deref: (*ptr).x:     %.2f\n", (*ptr).x);
    printf("Via arrow: ptr->y:       %.2f\n", ptr->y);

    // Byte offsets inside the struct (Memory Layout)
    printf("\nInternal Struct Memory Offsets (Flat Memory Model):\n");
    printf("  offsetof(Entity, id):    +%zu bytes (addr: %p)\n", offsetof(Entity, id), (void *)&ptr->id);
    printf("  offsetof(Entity, x):     +%zu bytes (addr: %p)\n", offsetof(Entity, x), (void *)&ptr->x);
    printf("  offsetof(Entity, y):     +%zu bytes (addr: %p)\n", offsetof(Entity, y), (void *)&ptr->y);
    printf("  offsetof(Entity, flags): +%zu bytes (addr: %p)\n", offsetof(Entity, flags), (void *)&ptr->flags);
    printf("  Total sizeof(Entity):    %zu bytes\n", sizeof(Entity));
}

/* ============================================================================
 * MODULE 4: Pointers to Pointers (**ptr) & Handles
 * ----------------------------------------------------------------------------
 * WHY DOUBLE POINTERS?
 *   1. You want a function to change WHERE a pointer points (e.g. buffer reallocation).
 *   2. 2D jagged arrays / pointer arrays (like `char **argv`).
 *   3. Handle tables in engines (`anti` handle -> slot address).
 * ============================================================================
 */
// Modifying a pointer inside a function requires passing the pointer's address (**p)
static void allocate_buffer(int32_t **out_buf, size_t count) {
    // In engine programming or standard C, allocate buffer and assign it back to caller
    *out_buf = (int32_t *)malloc(count * sizeof(int32_t));
    if (*out_buf != nullptr) {
        for (size_t i = 0; i < count; i++) {
            (*out_buf)[i] = (int32_t)(i * 10);
        }
    }
}

static void demo_module_4_pointer_to_pointer(void) {
    print_banner("MODULE 4: Pointer-to-Pointer (**ptr) & Dynamic Allocation");

    int32_t *my_buffer = nullptr;
    printf("Before allocate_buffer(): my_buffer = %p\n", (void *)my_buffer);

    // Pass the address of the pointer (&my_buffer -> int32_t**)
    allocate_buffer(&my_buffer, 5);

    printf("After allocate_buffer():  my_buffer = %p (Now points to heap memory!)\n", (void *)my_buffer);
    if (my_buffer != nullptr) {
        printf("Buffer contents: ");
        for (size_t i = 0; i < 5; i++) {
            printf("[%zu]=%d ", i, my_buffer[i]);
        }
        printf("\n");
        free(my_buffer);
        my_buffer = nullptr;
    }
}

/* ============================================================================
 * MODULE 5: void* and Byte-Level Pointer Math (Unsafe Memory)
 * ----------------------------------------------------------------------------
 * JAVA:       MemorySegment / Unsafe (raw addresses, byte offsets)
 * C23:        void* (untyped pointer to memory).
 * 
 * RULE:
 *   You cannot do arithmetic on 'void*' directly in standard C (sizeof(void) is undefined).
 *   Cast to 'uint8_t*' or 'char*' to do exact byte-by-byte arithmetic!
 * ============================================================================
 */
typedef struct AntiHeader {
    uint32_t type_tag;
    uint32_t length;
} AntiHeader;

static void demo_module_5_void_and_bytes(void) {
    print_banner("MODULE 5: void* & Byte Offsets (anti_mem Pattern)");

    // Simulate 'anti_mem_alloc': allocate header + payload in one contiguous block
    size_t payload_bytes = 16;
    size_t total_bytes = sizeof(AntiHeader) + payload_bytes;
    void *raw_block = malloc(total_bytes);
    assert(raw_block != nullptr);

    // 1. Write header at the start of block
    AntiHeader *hdr = (AntiHeader *)raw_block;
    hdr->type_tag = 0xAA55CC33;
    hdr->length = (uint32_t)payload_bytes;

    // 2. Compute payload pointer by stepping past header using uint8_t* byte arithmetic
    uint8_t *byte_ptr = (uint8_t *)raw_block;
    void *user_payload = (void *)(byte_ptr + sizeof(AntiHeader));

    printf("Raw Allocated Block: %p\n", raw_block);
    printf("Header Tag:          0x%08X (len=%u)\n", hdr->type_tag, hdr->length);
    printf("User Payload Addr:   %p (+%zu bytes from start)\n", user_payload, sizeof(AntiHeader));

    // 3. Recover header from user payload address (stepping backwards in memory!)
    uint8_t *user_bytes = (uint8_t *)user_payload;
    AntiHeader *recovered_hdr = (AntiHeader *)(user_bytes - sizeof(AntiHeader));

    printf("Recovered Header:    0x%08X (Matches: %s)\n",
           recovered_hdr->type_tag,
           recovered_hdr->type_tag == hdr->type_tag ? "YES!" : "NO!");

    free(raw_block);
}

/* ============================================================================
 * MODULE 6: The Const Pointer Matrix
 * ----------------------------------------------------------------------------
 * Read from right-to-left:
 *   const int *p   -> "p is a pointer to an int that is CONST" (data read-only)
 *   int *const p   -> "p is a CONST pointer to an int" (pointer address immutable)
 *   const int *const p -> "p is a CONST pointer to a CONST int" (both locked)
 * ============================================================================
 */
static void demo_module_6_const_matrix(void) {
    print_banner("MODULE 6: The Const Pointer Matrix");

    int a = 10;
    int b = 20;

    // 1. Pointer to const int (Can repoint, cannot write through)
    const int *ptr_to_const = &a;
    printf("1. const int *ptr:  *ptr_to_const = %d\n", *ptr_to_const);
    ptr_to_const = &b; // OK: Can point to another address
    printf("   Repointed to b:  *ptr_to_const = %d\n", *ptr_to_const);
    // *ptr_to_const = 30; // COMPILER ERROR! Read-only view.

    // 2. Const pointer to int (Cannot repoint, can write through)
    int *const const_ptr = &a;
    *const_ptr = 99; // OK: Can mutate data
    printf("2. int *const ptr:  wrote *const_ptr = 99 -> a is now %d\n", a);
    // const_ptr = &b; // COMPILER ERROR! Address is locked.

    // 3. Const pointer to const int
    const int *const locked_ptr = &b;
    printf("3. const int *const: fully locked at %p -> val=%d\n", (void *)locked_ptr, *locked_ptr);
}

/* ============================================================================
 * MODULE 7: Array Decay & The Function Parameter Trap
 * ----------------------------------------------------------------------------
 * TRAP: In C, when an array is passed into a function, it "decays" to a raw pointer.
 *       Inside the function, sizeof(arr) returns 8 (pointer size), NOT array size!
 * ============================================================================
 */
static void print_array_decay_trap(const int *decayed_arr) {
    // When passed as a parameter, the array syntax 'int arr[]' or 'const int *arr' is just a pointer!
    printf("  Inside function: sizeof(decayed_arr) = %zu bytes (POINTER SIZE in 64-bit!)\n", sizeof(decayed_arr));
}

static void demo_module_7_array_decay(void) {
    print_banner("MODULE 7: Array Decay Trap");

    int my_array[10] = {0};
    printf("  In caller scope: sizeof(my_array)    = %zu bytes (10 ints * 4 bytes)\n", sizeof(my_array));
    print_array_decay_trap(my_array);
    printf("  LESSON: In C, ALWAYS pass array length as an explicit parameter (size_t len)!\n");
}

/* ============================================================================
 * MODULE 8: Function Pointers (Java Lambdas / OOP Interfaces in C)
 * ----------------------------------------------------------------------------
 * JAVA:       interface Callback { void onEvent(int code); }
 * C23:        typedef void (*EventCallback)(int32_t code, void *userdata);
 * ============================================================================
 */
typedef int32_t (*BinaryOpFn)(int32_t a, int32_t b);

static int32_t op_add(int32_t a, int32_t b) { return a + b; }
static int32_t op_mul(int32_t a, int32_t b) { return a * b; }

static void demo_module_8_function_pointers(void) {
    print_banner("MODULE 8: Function Pointers & Callbacks");

    BinaryOpFn operation = op_add;
    printf("Using op_add: 10 + 5 = %d\n", operation(10, 5));

    operation = op_mul;
    printf("Using op_mul: 10 * 5 = %d\n", operation(10, 5));

    // Dispatch table (array of function pointers)
    BinaryOpFn table[2] = { op_add, op_mul };
    const char *names[2] = { "ADD", "MUL" };
    for (int i = 0; i < 2; i++) {
        printf("  Dispatch table[%d] (%s): result = %d\n", i, names[i], table[i](20, 4));
    }
}

/* ============================================================================
 * MODULE 9: Bit Masking & Tagged Pointers
 * ----------------------------------------------------------------------------
 * On 64-bit Apple Silicon (ARM64), pointers are aligned to 8 or 16 bytes.
 * The lowest 3 or 4 bits are ALWAYS 0!
 * We can pack type metadata or flags in the low bits or high bits of pointers.
 * ============================================================================
 */
static void demo_module_9_pointer_masking(void) {
    print_banner("MODULE 9: Bit-Packed / Tagged Pointers");

    uint64_t dummy_data = 0x12345678;
    void *ptr = &dummy_data;

    // Check alignment: 8-byte aligned means lowest 3 bits are 0
    uintptr_t raw_addr = (uintptr_t)ptr;
    printf("Raw pointer address: 0x%016lx\n", (unsigned long)raw_addr);
    printf("Lowest 3 bits:       0x%lx (All zeros due to alignment)\n", (unsigned long)(raw_addr & 0x7));

    // Tag the pointer with tag 3 (e.g. type tag)
    uintptr_t tag = 3;
    uintptr_t tagged_ptr = raw_addr | tag;
    printf("Tagged pointer:      0x%016lx\n", (unsigned long)tagged_ptr);

    // Extract tag and untag to restore original pointer
    uintptr_t extracted_tag = tagged_ptr & 0x7;
    void *untagged_ptr = (void *)(tagged_ptr & ~((uintptr_t)0x7));

    printf("Extracted Tag:       %lu\n", (unsigned long)extracted_tag);
    printf("Restored Pointer:    %p (Matches original: %s)\n",
           untagged_ptr, untagged_ptr == ptr ? "YES!" : "NO!");
}

/* ============================================================================
 * MODULE 10: Interactive Practice Exercises (Self-Verifying!)
 * ============================================================================
 */

// EXERCISE 1: Implement swap using pointers
static void exercise_1_swap(int32_t *a, int32_t *b) {
    int32_t temp = *a;
    *a = *b;
    *b = temp;
}

// EXERCISE 2: Compute strided sum (e.g. every 2nd element using pointer walk)
static int32_t exercise_2_strided_sum(const int32_t *arr, size_t count, size_t stride) {
    int32_t sum = 0;
    const int32_t *end = arr + count;
    for (const int32_t *p = arr; p < end; p += stride) {
        sum += *p;
    }
    return sum;
}

// EXERCISE 3: Modify caller pointer through double pointer
static void exercise_3_repoint(const char **str_ptr, const char *new_str) {
    *str_ptr = new_str;
}

static void run_practice_exercises(void) {
    print_banner("MODULE 10: Practice Exercises & Automated Tests");

    // Test 1: Swap
    int32_t x = 10, y = 20;
    exercise_1_swap(&x, &y);
    printf("[Test 1: Swap] x=%d, y=%d (Expected: 20, 10) -> ", x, y);
    assert(x == 20 && y == 10);
    printf("PASS\n");

    // Test 2: Strided Sum
    int32_t values[6] = {1, 100, 2, 200, 3, 300};
    int32_t sum = exercise_2_strided_sum(values, 6, 2); // 1 + 2 + 3 = 6
    printf("[Test 2: Strided Sum] sum=%d (Expected: 6) -> ", sum);
    assert(sum == 6);
    printf("PASS\n");

    // Test 3: Repoint
    const char *msg = "Original Message";
    exercise_3_repoint(&msg, "New Pointer Message");
    printf("[Test 3: Double Pointer Repoint] msg=\"%s\" -> ", msg);
    assert(strcmp(msg, "New Pointer Message") == 0);
    printf("PASS\n");

    printf("\n>>> ALL EXERCISE ASSERTIONS PASSED SUCCESSFULLY! <<<\n");
}

/* ============================================================================
 * MAIN ENTRY POINT
 * ============================================================================
 */
int main(void) {
    printf("====================================================================\n");
    printf("          ANTI ENGINE — C23 POINTER TRANSLATION WORKBENCH          \n");
    printf("====================================================================\n");

    demo_module_0_basics();
    demo_module_1_pass_by_address();
    demo_module_2_pointer_arithmetic();
    demo_module_3_struct_pointers();
    demo_module_4_pointer_to_pointer();
    demo_module_5_void_and_bytes();
    demo_module_6_const_matrix();
    demo_module_7_array_decay();
    demo_module_8_function_pointers();
    demo_module_9_pointer_masking();
    run_practice_exercises();

    printf("\n====================================================================\n");
    printf(" Finished running pointer translation lab!\n");
    printf("====================================================================\n");
    return 0;
}
