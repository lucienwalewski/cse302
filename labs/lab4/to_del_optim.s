	.globl x
	.globl y
	.globl function
	.globl z
	.globl main
.data
x:  .quad 10
y:  .quad 15
z:  .quad 1
.text
function :
	pushq %rbp
	movq %rsp, %rbp
	subq $64, %rsp
	movq %rdi, -72(%rbp)
	.L3:
	movq x(%rip), %r11
	movq %r11, -80(%rbp)
	movq -80(%rbp), %r11
	movq %r11, -88(%rbp)
	movq -88(%rbp), %rdi
	callq __bx_print_int
	movq $20, -96(%rbp)
	movq -96(%rbp), %r11
	movq %r11, -104(%rbp)
	movq -104(%rbp), %r11
	movq %r11, -88(%rbp)
	movq -88(%rbp), %rdi
	callq __bx_print_int
	.L0:
	movq $30, -112(%rbp)
	movq -112(%rbp), %r11
	movq %r11, -120(%rbp)
	movq -120(%rbp), %r11
	movq %r11, -88(%rbp)
	movq -88(%rbp), %rdi
	callq __bx_print_int
	.L2:
	movq -96(%rbp), %r11
	movq %r11, -128(%rbp)
	movq -128(%rbp), %r11
	movq %r11, -88(%rbp)
	movq -88(%rbp), %rdi
	callq __bx_print_int
	.KPiMt:
	movq %rbp, %rsp
	popq %rbp
	retq
main :
	pushq %rbp
	movq %rsp, %rbp
	subq $32, %rsp
	.L1:
	movq $5, -72(%rbp)
	movq -72(%rbp), %r11
	movq %r11, -80(%rbp)
	movq -80(%rbp), %rdi
	callq function
	movq x(%rip), %r11
	movq %r11, -88(%rbp)
	movq -88(%rbp), %r11
	movq %r11, -80(%rbp)
	movq -80(%rbp), %rdi
	callq __bx_print_int
	.BfWTX:
	movq %rbp, %rsp
	popq %rbp
	retq
