	.section .rodata
.lprintfmt:
	.string "%ld\n"
	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $120, %rsp
	.Lb12:
	movq $20, -8(%rbp)
	movq $0, -16(%rbp)
	movq $0, -24(%rbp)
	jmp .L0
	.L0:
	.L1:
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	movq $0, -40(%rbp)
	movq -32(%rbp), %r11
	subq -40(%rbp), %r11
	movq %r11, -32(%rbp)
	movq $0, %r11
	cmpq %r11, -32(%rbp)
	je .L3
	jmp .Lb13
	.Lb13:
	.L4:
	jmp .L5
	.L3:
	.L2:
	retq
	.L5:
	movq -8(%rbp), %r11
	movq %r11, -48(%rbp)
	pushq %rdi
	pushq %rax
	movq -48(%rbp), %rdi
	callq bx_print_int
	popq %rax
	popq %rdi
	movq $1, -16(%rbp)
	movq $0, -24(%rbp)
	jmp .L6
	.L6:
	.L7:
	movq -16(%rbp), %r11
	movq %r11, -56(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -64(%rbp)
	movq -56(%rbp), %r11
	subq -64(%rbp), %r11
	movq %r11, -56(%rbp)
	movq $0, %r11
	cmpq %r11, -56(%rbp)
	jg .L9
	jmp .Lb15
	.Lb15:
	.L10:
	jmp .L11
	.L9:
	.L8:
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
	jmp .L0
	.L11:
	movq -24(%rbp), %r11
	movq %r11, -96(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -104(%rbp)
	movq -96(%rbp), %r11
	addq -104(%rbp), %r11
	movq %r11, -24(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -112(%rbp)
	movq $1, -120(%rbp)
	movq -112(%rbp), %r11
	addq -120(%rbp), %r11
	movq %r11, -16(%rbp)
	jmp .L6
	movq %rbp, %rsp
	popq %rbp
	xorq %rax, %rax
	retq
