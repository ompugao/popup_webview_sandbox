let s:Job = vital#popupapp#import('System.Job')

function! s:on_stdout(data) abort dict
	let self.stdout[-1] .= a:data[0]
	call extend(self.stdout, a:data[1:])
endfunction

function! s:on_stderr(data) abort dict
	let self.stderr[-1] .= a:data[0]
	call extend(self.stderr, a:data[1:])
endfunction

function! s:on_exit(exitval) abort dict
	let self.exit_status = a:exitval
endfunction

function! popupapp#start() abort
	if !exists('s:job')
		let s:job = s:Job.start(['popupapp'], {
					\ 'stdout': [''],
					\ 'stderr': [''],
					\ 'exit_status': -1,
					\ 'on_stdout': function('s:on_stdout'),
					\ 'on_stderr': function('s:on_stderr'),
					\ 'on_exit': function('s:on_exit'),
					\})
	endif
endfunction

function! popupapp#show_image(path) abort
	call popupapp#start()
	call s:job.send('image ' . a:path . "\n")
endfunction

function! popupapp#show_youtube(url) abort
	call popupapp#start()
	call s:job.send('youtube ' . a:url . "\n")
endfunction

function! popupapp#show() abort
	call popupapp#start()
	call s:job.send("show\n")
endfunction

function! popupapp#hide() abort
	call popupapp#start()
	call s:job.send("hide\n")
endfunction

function! popupapp#stop() abort
	if exists('s:job')
		" call s:job.send('close' . "\n")
		call s:job.stop()
		call s:job.wait()
		unlet s:job
	endif
endfunction
