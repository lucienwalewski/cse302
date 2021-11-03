	.globl x
	.globl y
	.globl fizzbuzz
	.globl z
	.globl main
.data
x:  .quad 10
y:  .quad 15
z:  .quad 1
.text
fizzbuzz :
	pushq %rbp
	movq %rsp, %rbp
	subq $216, %rsp
	pushq %rbp
	movq %rsp, %rbp
	movq %rdi, -8(%rbp)
	movq %rsi, -16(%rbp)
	.L0:
	movq -8(%rbp), %r11
	movq %r11, -24(%rbp)
	movq -16(%rbp), %r11
	movq %r11, -32(%rbp)
	movq -24(%rbp), %r11
	subq -32(%rbp), %r11
	movq %r11, -24(%rbp)
	movq $0, %r11
	cmpq %r11, -24(%rbp)
	jle .L1
	jmp .L2
	.L1:
	movq -8(%rbp), %r11
	movq %r11, -40(%rbp)
	movq $3, -48(%rbp)
	movq -40(%rbp), %rax
	cqto
	idivq -48(%rbp)
	movq %rdx, -56(%rbp)
	movq $0, -64(%rbp)
	movq -56(%rbp), %r11
	subq -64(%rbp), %r11
	movq %r11, -56(%rbp)
	movq $0, %r11
	cmpq %r11, -56(%rbp)
	je .L3
	jmp .L4
	.L3:
	movq -8(%rbp), %r11
	movq %r11, -72(%rbp)
	movq $5, -80(%rbp)
	movq -72(%rbp), %rax
	cqto
	idivq -80(%rbp)
	movq %rdx, -88(%rbp)
	movq $0, -96(%rbp)
	movq -88(%rbp), %r11
	subq -96(%rbp), %r11
	movq %r11, -88(%rbp)
	movq $0, %r11
	cmpq %r11, -88(%rbp)
	je .L6
	jmp .L7
	.L6:
	movq $151515, -104(%rbp)
	movq -104(%rbp), %r11
	movq %r11, -112(%rbp)
	movq -120(%rbp), %rdi
	callq __bx_print_int
	addq $-39, %rsp
	jmp .L8
	.L7:
	movq $333, -128(%rbp)
	movq -128(%rbp), %r11
	movq %r11, -112(%rbp)
	movq -120(%rbp), %rdi
	callq __bx_print_int
	addq $-39, %rsp
	.L8:
	jmp .L5
	.L4:
	movq -8(%rbp), %r11
	movq %r11, -136(%rbp)
	movq $5, -144(%rbp)
	movq -136(%rbp), %rax
	cqto
	idivq -144(%rbp)
	movq %rdx, -152(%rbp)
	movq $0, -160(%rbp)
	movq -152(%rbp), %r11
	subq -160(%rbp), %r11
	movq %r11, -152(%rbp)
	movq $0, %r11
	cmpq %r11, -152(%rbp)
	je .L9
	jmp .L10
	.L9:
	movq $555, -168(%rbp)
	movq -168(%rbp), %r11
	movq %r11, -112(%rbp)
	movq -120(%rbp), %rdi
	callq __bx_print_int
	addq $-39, %rsp
	jmp .L11
	.L10:
	movq -8(%rbp), %r11
	movq %r11, -176(%rbp)
	movq -176(%rbp), %r11
	movq %r11, -112(%rbp)
	movq -120(%rbp), %rdi
	callq __bx_print_int
	addq $-39, %rsp
	.L11:
	.L5:
	movq -8(%rbp), %r11
	movq %r11, -184(%rbp)
	movq $1, -192(%rbp)
	movq -184(%rbp), %r11
	addq -192(%rbp), %r11
	movq %r11, -8(%rbp)
	jmp .L0
	.L2:
	movq x(%rip), %r11
	movq %r11, -200(%rbp)
	movq y(%rip), %r11
	movq %r11, -208(%rbp)
	movq -200(%rbp), %r11
	addq -208(%rbp), %r11
	movq %r11, y(%rip)
	movq -8(%rbp), %r11
	movq %r11, -216(%rbp)
	movq -216(%rbp), %rax 
	jmp .DopGM
	.DopGM:
	movq %rbp, %rsp
	popq %rbp
	retq
main :
	pushq %rbp
	movq %rsp, %rbp
	subq $40, %rsp
	pushq %rbp
	movq %rsp, %rbp
	movq $0, -8(%rbp)
	movq -8(%rbp), %r11
	movq %r11, -16(%rbp)
	movq $100, -24(%rbp)
	movq -24(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -32(%rbp), %rdi
	movq -32(%rbp), %rsi
	callq fizzbuzz
	addq $-32, %rsp
	movq %rax, x
	movq x(%rip), %r11
	movq %r11, -40(%rbp)
	movq -40(%rbp), %r11
	movq %r11, -16(%rbp)
	movq -32(%rbp), %rdi
	callq __bx_print_int
	addq $-39, %rsp
	.SSBgQ:
	movq %rbp, %rsp
	popq %rbp
	retq
