// Lean compiler output
// Module: Leansoln.data
// Imports: Init
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
static lean_object* l_data___closed__1;
LEAN_EXPORT lean_object* l_data;
static lean_object* _init_l_data___closed__1() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("+13\n-18\n+13\n+10\n+12\n-4\n+17\n-16\n-6\n+10\n+4\n-1\n+7\n+13\n-1\n+16\n-7\n-6\n+18\n-6\n+13\n-8\n+2\n+16\n-5\n-14\n-5\n-2\n+11\n+17\n+17\n+9\n-14\n-17\n+7\n+16\n-15\n-13\n-13\n-11\n+1\n+6\n-5\n-4\n-19\n+9\n-7\n-18\n+7\n+8\n-17\n-6\n-12\n+9\n-12\n-13\n+5\n-12\n+8\n+9\n+5\n+11\n-19\n+11\n-16\n+15\n-18\n-12\n+19\n-18\n-7\n+5\n-9\n+13\n+13\n+8\n-16\n+3\n-16\n+7\n-9\n-12\n-18\n-12\n+14\n+18\n-11\n+2\n+11\n-18\n-3\n+5\n-8\n+18\n+12\n+18\n+8\n+4\n+25\n-13\n+11\n+7\n-8\n+16\n+14\n-7\n-16\n+22\n-12\n-8\n+19\n+6\n+5\n+8\n+1\n+26\n+17\n+14\n+13\n+18\n+5\n-17\n-1\n+6\n-1\n-3\n-18\n-6\n+15\n+16\n+7\n+18\n+8\n+13\n+3\n-18\n-9\n-17\n+13\n-5\n+2\n-5\n+11\n-9\n+4\n+13\n+8\n+2\n-11\n-11\n-22\n+13\n-19\n-19\n+18\n+10\n+3\n+10\n+21\n-13\n+16\n+1\n+15\n+17\n+17\n-5\n+16\n+17\n+10\n+4\n+1\n-3\n-14\n+18\n-17\n-6\n-9\n+17\n-6\n+1\n-17\n+7\n-6\n+2\n+3\n-11\n-16\n-17\n-11\n-1\n-2\n-17\n+22\n+3\n+12\n-13\n+8\n+20\n+8\n+6\n-1\n-4\n+19\n+17\n+13\n+8\n+4\n+6\n+20\n+9\n+2\n-3\n+18\n+6\n-18\n-8\n+13\n-4\n+3\n+13\n+15\n-7\n+11\n-15\n+7\n-17\n+9\n+18\n+15\n-12\n+11\n+6\n+7\n-17\n+18\n-4\n-1\n-15\n-15\n+4\n-12\n+11\n+15\n-12\n-13\n-17\n+1\n+2\n+3\n-17\n+10\n-7\n-6\n+10\n-20\n-11\n-15\n+8\n-2\n-12\n+18\n-16\n-8\n+4\n+13\n+20\n-15\n+11\n+12\n-16\n+15\n-12\n-13\n+12\n-17\n+16\n+23\n-18\n-12\n+2\n+11\n+3\n-13\n+17\n+21\n-24\n+6\n+11\n-23\n-18\n-28\n-1\n-2\n+16\n+4\n-13\n+18\n-16\n-3\n+5\n+17\n-4\n-7\n-13\n-9\n-16\n-8\n-7\n+22\n-19\n-10\n+6\n+3\n+23\n-4\n+5\n-15\n-17\n-8\n-8\n+6\n+6\n-2\n-15\n+12\n+6\n-11\n-9\n-9\n+15\n-26\n-6\n-18\n-7\n-19\n-2\n+1\n+3\n+12\n-11\n-23\n-4\n-15\n+9\n-14\n-5\n-28\n-9\n+16\n+22\n+7\n-16\n+7\n-1\n+17\n-12\n+18\n+12\n-10\n+4\n-5\n+14\n-12\n-6\n+25\n+13\n-10\n-9\n+13\n+21\n-17\n-9\n-4\n+18\n-24\n-1\n-14\n+10\n+42\n+24\n-7\n-6\n+12\n+8\n+4\n+24\n-4\n+18\n+1\n-24\n+21\n+17\n+16\n+51\n-21\n+70\n-8\n+15\n+16\n+2\n-3\n+10\n+19\n+15\n+8\n+21\n+11\n+10\n-2\n-7\n-7\n+5\n-19\n+7\n-16\n-1\n+2\n-14\n-4\n-14\n+19\n-7\n-11\n+7\n+5\n-10\n-15\n+4\n-10\n-11\n-13\n-11\n+12\n+13\n-10\n+3\n+18\n-9\n+1\n+12\n+12\n+18\n-6\n+4\n-5\n-3\n+18\n+1\n-4\n-33\n+17\n-4\n+7\n-13\n+52\n-3\n-3\n-18\n-3\n-5\n+13\n+9\n+18\n+23\n-21\n-15\n-16\n-23\n-9\n-4\n-40\n-3\n+86\n+18\n-2\n+27\n-1\n-12\n+71\n-8\n+20\n+37\n-36\n+43\n-40\n-69\n-13\n+35\n+4\n+6\n-17\n-178\n-56\n-14\n-243\n+3\n+204\n-22\n+517\n-71500\n-244\n-6\n+19\n-18\n+1\n+19\n-23\n-18\n+10\n+6\n-14\n+9\n-7\n+19\n-11\n-5\n+23\n+8\n-6\n-18\n-20\n-18\n-7\n+2\n-11\n+8\n-18\n+7\n-14\n+15\n-19\n-17\n-10\n-12\n-6\n+10\n-6\n+5\n-7\n+5\n-11\n-2\n-15\n+10\n+1\n-9\n+18\n+14\n-10\n-12\n-13\n+19\n-15\n-10\n-5\n-16\n-12\n+14\n-15\n-4\n-9\n-9\n-11\n-6\n+2\n+17\n+11\n-5\n+19\n+18\n-19\n+3\n+3\n+11\n-3\n+12\n+7\n+5\n-10\n-4\n-6\n-2\n+7\n-3\n-7\n+19\n+2\n+9\n-8\n+9\n-15\n-2\n+18\n-23\n-23\n-15\n-6\n+17\n+17\n-5\n+14\n-13\n-18\n-11\n-10\n-19\n-5\n-13\n+12\n-5\n+16\n+15\n-6\n-16\n-8\n-21\n-2\n+7\n-3\n-16\n-6\n+14\n+7\n+3\n+5\n-19\n+6\n+7\n+11\n-2\n+4\n-9\n-16\n-4\n-15\n-6\n+7\n-12\n-8\n-13\n-8\n+9\n+3\n+4\n-6\n+14\n+13\n-15\n-18\n-3\n-2\n+19\n-1\n+8\n-14\n+3\n-17\n-13\n-2\n+12\n-2\n+15\n+13\n+22\n-3\n+8\n+16\n-13\n+15\n-13\n-6\n-18\n+10\n-7\n-5\n+7\n+12\n-1\n+5\n+2\n+10\n+17\n+22\n-10\n-5\n+25\n+5\n-13\n-10\n-16\n+19\n-9\n+5\n+20\n+10\n-1\n+9\n-5\n+23\n-17\n-14\n-18\n+9\n-20\n+14\n+36\n+16\n+11\n-24\n-2\n-3\n-1\n+20\n-3\n+8\n+21\n+11\n+17\n+14\n+8\n+3\n+18\n-15\n+8\n-16\n+12\n+8\n+13\n+16\n-3\n-16\n+7\n-15\n+5\n-2\n+6\n+10\n-5\n+2\n-4\n+18\n+15\n-3\n-17\n+4\n+8\n+15\n-19\n-11\n+19\n-1\n+14\n-19\n+8\n+3\n+10\n+16\n-23\n+2\n-4\n-9\n+12\n+18\n-32\n+8\n-16\n+25\n+2\n+4\n-41\n-8\n-3\n-19\n+9\n-2\n+1\n-9\n+4\n-17\n-9\n+11\n+3\n+20\n-17\n-9\n+16\n-18\n-9\n-12\n+5\n-3\n+16\n-23\n+59\n-23\n+12\n-16\n-8\n+15\n+8\n+25\n-77\n-48\n+1\n-26\n+9\n-17\n-13\n-29\n-7\n-3\n-22\n+18\n-21\n-26\n-17\n+2\n+11\n+11\n+6\n+11\n+13\n+13\n+23\n+24\n+2\n+17\n-48\n-38\n-21\n-10\n+18\n-27\n-19\n+6\n+12\n-14\n-5\n+2\n+8\n-14\n-7\n+2\n-18\n-10\n-12\n+13\n+2\n-18\n+10\n+3\n+13\n+6\n-1\n-4\n-20\n+4\n-12\n+9\n-3\n+1\n+14\n+17\n-2\n-12\n+7\n-16\n-2\n-14\n-18\n-5\n+17\n-10\n+7\n+5\n-7\n-3\n-13\n+15\n+7\n-5\n-18\n+4\n-14\n-9\n-13\n-16\n-8\n-6\n+10\n-1\n+19\n+14\n-13\n+4\n+13\n-9\n+8\n+6\n-2\n-15\n+13\n-8\n+21\n+11\n-18\n+16\n-10\n+6\n+3\n+20\n+8\n-9\n-12\n-20\n+18\n-12\n-13\n-13\n+3\n-2\n-10\n-1\n+19\n-4\n-9\n-7\n+3\n-4\n-18\n-16\n+19\n-12\n+16\n+5\n+15\n-11\n-6\n-21\n+4\n-19\n-13\n+10\n+4\n+7\n-43\n+34\n+40\n+23\n+9\n+14\n+19\n+11\n+22\n+9\n-11\n+22\n+11\n+11\n-20\n-17\n+7\n+15\n-23\n+6\n-17\n-8\n-8\n-4\n+24\n+18\n+8\n+17\n-22\n+19\n+71889", 3500, 3500);
return x_1;
}
}
static lean_object* _init_l_data() {
_start:
{
lean_object* x_1; 
x_1 = l_data___closed__1;
return x_1;
}
}
lean_object* initialize_Init(uint8_t builtin, lean_object*);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_Leansoln_data(uint8_t builtin, lean_object* w) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin, lean_io_mk_world());
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
l_data___closed__1 = _init_l_data___closed__1();
lean_mark_persistent(l_data___closed__1);
l_data = _init_l_data();
lean_mark_persistent(l_data);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
