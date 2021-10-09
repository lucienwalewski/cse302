	.section .rodata
.lprintfmt:
	.string "%ld\n"
	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $88, %rsp
	movq $20, -8(%rbp)
	movq $0, -16(%rbp)
	movq $0, -24(%rbp)
	0:
	jmp 1
	1:
	3:
	jmp 2
	jmp 5
	4:
	5:
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	pushq %rdi
	pushq %rax
	movq -32(%rbp), %rdi
	callq bx_print_int
	popq %rax
	popq %rdi
	movq $1, -16(%rbp)
	movq $0, -24(%rbp)
	6:
	jmp 7
	7:
	9:
	jmp 8
	jmp 11
	10:
	11:
	movq -24(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -48(%rbp)
	movq -40(%rbp), %r11
	addq -48(%rbp), %r11
	movq %r11, -24(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -56(%rbp)
	movq $1, -64(%rbp)
	movq -56(%rbp), %r11
	addq -64(%rbp), %r11
	movq %r11, -16(%rbp)
	jmp 6
	8:
	movq -24(%rbp), %r11
	movq %r11, -72(%rbp)
	pushq %rdi
	pushq %rax
	movq -72(%rbp), %rdi
	callq bx_print_int
	popq %rax
	popq %rdi
	movq -8(%rbp), %r11
	movq %r11, -80(%rbp)
	movq $1, -88(%rbp)
	movq -80(%rbp), %r11
	subq -88(%rbp), %r11
	movq %r11, -8(%rbp)
	jmp 0
	2:
	movq %rbp, %rsp
	popq %rbp
	xorq %rax, %rax
	retq
