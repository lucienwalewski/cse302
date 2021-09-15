	.section .rodata
.lprintfmt:
	.string "%ld\n"
	.text
	.globl main
main:
	pushq %rbp
	movq %rsp, %rbp
	subq $40, %rsp
	movq $0, -8(%rbp)
	movq $0, -16(%rbp)
	movq $0, -24(%rbp)
	movq $1, -16(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -32(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -32(%rbp), %r11
	addq -40(%rbp), %r11
	movq %r11, -24(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -8(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -32(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -32(%rbp), %r11
	addq -40(%rbp), %r11
	movq %r11, -24(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -8(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -32(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -32(%rbp), %r11
	addq -40(%rbp), %r11
	movq %r11, -24(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -8(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -32(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -32(%rbp), %r11
	addq -40(%rbp), %r11
	movq %r11, -24(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -8(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -32(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -32(%rbp), %r11
	addq -40(%rbp), %r11
	movq %r11, -24(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -8(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -32(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -32(%rbp), %r11
	addq -40(%rbp), %r11
	movq %r11, -24(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -8(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -32(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -32(%rbp), %r11
	addq -40(%rbp), %r11
	movq %r11, -24(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -8(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -32(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -40(%rbp)
	movq -32(%rbp), %r11
	addq -40(%rbp), %r11
	movq %r11, -24(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -8(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -32(%rbp)
	leaq .lprintfmt(%rip), %rdi
	movq -32(%rbp), %rsi
	xorq %rax, %rax
	callq printf@PLT
	movq %rbp, %rsp
	popq %rbp
	xorq %rax, %rax
	retq
