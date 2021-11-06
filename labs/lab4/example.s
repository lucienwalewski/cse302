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
	subq $208, %rsp
	movq %rdi, -72(%rbp)
	movq %rsi, -80(%rbp)
	.L0:
	movq -72(%rbp), %r11
	movq %r11, -88(%rbp)
	movq -80(%rbp), %r11
	movq %r11, -96(%rbp)
	movq -88(%rbp), %r11
	subq -96(%rbp), %r11
	movq %r11, -88(%rbp)
	movq $0, %r11
	cmpq %r11, -88(%rbp)
	jle .L1
	jmp .L2
	.L1:
	movq -72(%rbp), %r11
	movq %r11, -104(%rbp)
	movq $3, -112(%rbp)
	movq -104(%rbp), %rax
	cqto
	idivq -112(%rbp)
	movq %rdx, -120(%rbp)
	movq $0, -128(%rbp)
	movq -120(%rbp), %r11
	subq -128(%rbp), %r11
	movq %r11, -120(%rbp)
	movq $0, %r11
	cmpq %r11, -120(%rbp)
	je .L3
	jmp .L4
	.L3:
	movq -72(%rbp), %r11
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
	je .L6
	jmp .L7
	.L6:
	movq $151515, -168(%rbp)
	movq -168(%rbp), %r11
	movq %r11, -176(%rbp)
	movq -176(%rbp), %rdi
	callq __bx_print_int
	jmp .L8
	.L7:
	movq $333, -184(%rbp)
	movq -184(%rbp), %r11
	movq %r11, -176(%rbp)
	movq -176(%rbp), %rdi
	callq __bx_print_int
	.L8:
	jmp .L5
	.L4:
	movq -72(%rbp), %r11
	movq %r11, -192(%rbp)
	movq $5, -200(%rbp)
	movq -192(%rbp), %rax
	cqto
	idivq -200(%rbp)
	movq %rdx, -208(%rbp)
	movq $0, -216(%rbp)
	movq -208(%rbp), %r11
	subq -216(%rbp), %r11
	movq %r11, -208(%rbp)
	movq $0, %r11
	cmpq %r11, -208(%rbp)
	je .L9
	jmp .L10
	.L9:
	movq $555, -224(%rbp)
	movq -224(%rbp), %r11
	movq %r11, -176(%rbp)
	movq -176(%rbp), %rdi
	callq __bx_print_int
	jmp .L11
	.L10:
	movq -72(%rbp), %r11
	movq %r11, -232(%rbp)
	movq -232(%rbp), %r11
	movq %r11, -176(%rbp)
	movq -176(%rbp), %rdi
	callq __bx_print_int
	.L11:
	.L5:
	movq -72(%rbp), %r11
	movq %r11, -240(%rbp)
	movq $1, -248(%rbp)
	movq -240(%rbp), %r11
	addq -248(%rbp), %r11
	movq %r11, -72(%rbp)
	jmp .L0
	.L2:
	movq x(%rip), %r11
	movq %r11, -256(%rbp)
	movq y(%rip), %r11
	movq %r11, -264(%rbp)
	movq -256(%rbp), %r11
	addq -264(%rbp), %r11
	movq %r11, y(%rip)
	movq -72(%rbp), %r11
	movq %r11, -272(%rbp)
	movq -272(%rbp), %rax 
	jmp .xSvie
	.xSvie:
	movq %rbp, %rsp
	popq %rbp
	retq
main :
	pushq %rbp
	movq %rsp, %rbp
	subq $48, %rsp
	movq $0, -72(%rbp)
	movq -72(%rbp), %r11
	movq %r11, -80(%rbp)
	movq $100, -88(%rbp)
	movq -88(%rbp), %r11
	movq %r11, -96(%rbp)
	movq -80(%rbp), %rdi
	movq -96(%rbp), %rsi
	callq fizzbuzz
	movq %rax, x(%rip)
	movq x(%rip), %r11
	movq %r11, -104(%rbp)
	movq -104(%rbp), %r11
	movq %r11, -80(%rbp)
	movq -80(%rbp), %rdi
	callq __bx_print_int
	.tdDSV:
	movq %rbp, %rsp
	popq %rbp
	retq
