	.globl function
	.globl main
.data
.text
function :
	pushq %rbp
	movq %rsp, %rbp
	subq $112, %rsp
	movq %rdi, -72(%rbp)
	movq %rsi, -80(%rbp)
	movq %rdx, -88(%rbp)
	movq %rcx, -96(%rbp)
	movq %r8, -104(%rbp)
	movq %r9, -112(%rbp)
	
	movq 24(%rbp), %r11
	movq %r11, -120(%rbp)
	movq 32(%rbp), %r11
	movq %r11, -128(%rbp)
	movq 40(%rbp), %r11
	movq %r11, -136(%rbp)
	movq 48(%rbp), %r11
	movq %r11, -144(%rbp)
	movq 56(%rbp), %r11
	movq %r11, -152(%rbp)
	movq -120(%rbp), %r11
	movq %r11, -160(%rbp)
	movq -160(%rbp), %r11
	movq %r11, -168(%rbp)
	movq -168(%rbp), %rdi
	callq __bx_print_int
	movq -128(%rbp), %r11
	movq %r11, -176(%rbp)
	movq -176(%rbp), %r11
	movq %r11, -168(%rbp)
	movq -168(%rbp), %rdi
	callq __bx_print_int
	xorq %rax, %rax
	jmp .vRUUu
	.vRUUu:
	movq %rbp, %rsp
	popq %rbp
	retq
main :
	pushq %rbp
	movq %rsp, %rbp
	subq $176, %rsp
	movq $1, -72(%rbp)
	movq $2, -80(%rbp)
	movq $3, -88(%rbp)
	movq $4, -96(%rbp)
	movq $5, -104(%rbp)
	movq $6, -112(%rbp)
	movq $7, -120(%rbp)
	movq $8, -128(%rbp)
	movq $9, -136(%rbp)
	movq $10, -144(%rbp)
	movq $11, -152(%rbp)
	movq -72(%rbp), %r11
	movq %r11, -160(%rbp)
	movq -80(%rbp), %r11
	movq %r11, -168(%rbp)
	movq -88(%rbp), %r11
	movq %r11, -176(%rbp)
	movq -96(%rbp), %r11
	movq %r11, -184(%rbp)
	movq -104(%rbp), %r11
	movq %r11, -192(%rbp)
	movq -112(%rbp), %r11
	movq %r11, -200(%rbp)
	movq -120(%rbp), %r11
	movq %r11, -208(%rbp)
	movq -128(%rbp), %r11
	movq %r11, -216(%rbp)
	movq -136(%rbp), %r11
	movq %r11, -224(%rbp)
	movq -144(%rbp), %r11
	movq %r11, -232(%rbp)
	movq -152(%rbp), %r11
	movq %r11, -240(%rbp)
	movq -160(%rbp), %rdi
	movq -168(%rbp), %rsi
	movq -176(%rbp), %rdx
	movq -184(%rbp), %rcx
	movq -192(%rbp), %r8
	movq -200(%rbp), %r9
	pushq -240(%rbp)
	pushq -232(%rbp)
	pushq -224(%rbp)
	pushq -216(%rbp)
	pushq -208(%rbp)
	
	callq function
	addq $48, %rsp
	xorq %rax, %rax
	jmp .XzCkN
	.XzCkN:
	movq %rbp, %rsp
	popq %rbp
	retq
