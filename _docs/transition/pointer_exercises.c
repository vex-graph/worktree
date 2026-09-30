/*
 * ============================================================================
 * pointer_exercises.c — Hands-on Pointer Practice & Challenge Exercises
 * ============================================================================
 * 
 * Instructions:
 *   Each exercise has a TODO function. Complete or inspect the implementation
 *   and run the _test suite to verify all assertions pass!
 * 
 * Build and run:
 *   clang -std=c23 -Wall -Wextra -Werror -mcpu=native pointer_exercises.c -o pointer_exercises  # portable across Apple Silicon; baseline apple-m1 if strict
 *   ./pointer_exercises
 * ============================================================================
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

// ============================================================================
// EXERCISE 1: Pointer-based In-Place Array Reversal
// Task: Reverse an array in-place using two pointers (head and tail)
// ============================================================================
static void reverse_array_with_pointers(int32_t *arr, size_t len) {
    if (len <= 1 || arr == nullptr)
        return;

    int32_t *left = arr;
    int32_t *right = arr + (len - 1);

    while (left < right) {
        int32_t temp = *left;
        *left = *right;
        *right = temp;

        left++;  // advances by sizeof(int32_t) bytes
        right--; // steps backward by sizeof(int32_t) bytes
    }
}

// ============================================================================
// EXERCISE 2: Negative Pointer Math (anti_mem Pattern)
// Task: Given a pointer to user payload, recover the header located immediately
//       before it in RAM.
// ============================================================================
typedef struct {
    uint32_t magic;
    uint32_t size_in_bytes;
} BlockHeader;

static BlockHeader *recover_header(void *payload_ptr) {
    uint8_t *byte_ptr = (uint8_t *)payload_ptr;
    // Step backward by sizeof(BlockHeader) bytes:
    return (BlockHeader *)(byte_ptr - sizeof(BlockHeader));
}

// ============================================================================
// EXERCISE 3: Reallocate Pointer via Double Pointer
// Task: Take a pointer-to-pointer, free the old buffer, and allocate a new one.
// ============================================================================
static void reallocate_buffer(int32_t **buf_ptr, size_t old_count, size_t new_count) {
    int32_t *new_buf = (int32_t *)malloc(new_count * sizeof(int32_t));
    assert(new_buf != nullptr);

    size_t copy_count = old_count < new_count ? old_count : new_count;
    if (*buf_ptr != nullptr) {
        memcpy(new_buf, *buf_ptr, copy_count * sizeof(int32_t));
        free(*buf_ptr);
    }

    // Zero _out remaining new elements
    for (size_t i = copy_count; i < new_count; i++) {
        new_buf[i] = 0;
    }

    // Update caller's pointer!
    *buf_ptr = new_buf;
}

// ============================================================================
// EXERCISE 4: Strided Matrix Row / Column Traversal
// Task: Sum elements along a specific column in a flat 1D row-major 2D array.
// ============================================================================
static int32_t sum_matrix_column(const int32_t *matrix, size_t rows, size_t cols, size_t target_col) {
    int32_t sum = 0;
    // Base pointer points at row 0, target_col
    const int32_t *ptr = matrix + target_col;

    for (size_t r = 0; r < rows; r++) {
        sum += *ptr;
        ptr += cols; // Stride jump by 'cols' elements to next row
    }
    return sum;
}

// ============================================================================
// EXERCISE 5: Bit-Packed Tag Extraction & Restoration
// Task: Pack a 3-bit tag (0..7) into the lower bits of an 8-byte aligned pointer.
// ============================================================================
static uintptr_t pack_pointer_tag(void *ptr, uint8_t tag) {
    uintptr_t raw = (uintptr_t)ptr;
    assert((raw & 0x7) == 0); // Must be 8-byte aligned
    return raw | (tag & 0x7);
}

static void *unpack_pointer(uintptr_t tagged_ptr, uint8_t *out_tag) {
    *out_tag = (uint8_t)(tagged_ptr & 0x7);
    return (void *)(tagged_ptr & ~((uintptr_t)0x7));
}

// ============================================================================
// TEST HARNESS
// ============================================================================
int main(void) {
    printf("====================================================================\n");
    printf("           POINTER PRACTICE & CHALLENGE TEST SUITE                 \n");
    printf("====================================================================\n\n");

    // 1. Reverse Array
    int32_t arr[5] = {1, 2, 3, 4, 5};
    reverse_array_with_pointers(arr, 5);
    printf("[1/5] Reverse Array: %d %d %d %d %d -> ", arr[0], arr[1], arr[2], arr[3], arr[4]);
    assert(arr[0] == 5 && arr[1] == 4 && arr[2] == 3 && arr[3] == 2 && arr[4] == 1);
    printf("PASS\n");

    // 2. Recover Header
    size_t alloc_sz = sizeof(BlockHeader) + 32;
    void *raw = malloc(alloc_sz);
    BlockHeader *hdr = (BlockHeader *)raw;
    hdr->magic = 0xDEADBEEF;
    hdr->size_in_bytes = 32;
    void *payload = (uint8_t *)raw + sizeof(BlockHeader);

    BlockHeader *recovered = recover_header(payload);
    printf("[2/5] Recover Header: Magic=0x%08X Size=%u -> ", recovered->magic, recovered->size_in_bytes);
    assert(recovered->magic == 0xDEADBEEF && recovered->size_in_bytes == 32);
    printf("PASS\n");
    free(raw);

    // 3. Double Pointer Reallocate
    int32_t *buf = nullptr;
    reallocate_buffer(&buf, 0, 3);
    buf[0] = 10; buf[1] = 20; buf[2] = 30;
    reallocate_buffer(&buf, 3, 5); // Grow to 5
    printf("[3/5] Reallocate Buffer (Double Pointer): [%d, %d, %d, %d, %d] -> ",
           buf[0], buf[1], buf[2], buf[3], buf[4]);
    assert(buf[0] == 10 && buf[1] == 20 && buf[2] == 30 && buf[3] == 0 && buf[4] == 0);
    printf("PASS\n");
    free(buf);

    // 4. Matrix Column Striding
    // 3x3 Matrix:
    //  1  2  3
    //  4  5  6
    //  7  8  9
    int32_t mat[3 * 3] = {
        1, 2, 3,
        4, 5, 6,
        7, 8, 9
    };
    int32_t col1_sum = sum_matrix_column(mat, 3, 3, 1); // 2 + 5 + 8 = 15
    printf("[4/5] Matrix Column Stride (Col 1 Sum): %d (Expected: 15) -> ", col1_sum);
    assert(col1_sum == 15);
    printf("PASS\n");

    // 5. Bit-Packed Tagging
    uint64_t dummy = 42;
    uintptr_t tagged = pack_pointer_tag(&dummy, 5);
    uint8_t extracted_tag = 0;
    void *restored = unpack_pointer(tagged, &extracted_tag);
    printf("[5/5] Bit-Packed Pointer: Tag=%u, Restored Addr=%p -> ", extracted_tag, restored);
    assert(extracted_tag == 5 && restored == &dummy);
    printf("PASS\n");

    std::cout << "hello world!";

    printf("\n====================================================================\n");
    printf(" ALL 5 POINTER EXERCISES PASSED! READY FOR THE ANTI ENGINE CORE!\n");
    printf("====================================================================\n");
    return 0;
}
