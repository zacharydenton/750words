" word wrap options
set tw=72 fo=cqt wm=0

"-------------- word count ---------------
" from http://stackoverflow.com/questions/114431/fast-word-count-function-in-vim/120386#120386

"returns the count of how many words are in the entire file excluding the current line
"updates the buffer variable Global_Word_Count to reflect this
fu! OtherLineWordCount()
	let data = []
	"get lines above and below current line unless current line is first or last
	if line(".") > 1
		let data = getline(1, line(".")-1)
	endif
	if line(".") < line("$")
		let data = data + getline(line(".")+1, "$")
	endif
	let count_words = 0
	let pattern = "\\<\\(\\w\\|-\\|'\\)\\+\\>"
	for str in data
		let count_words = count_words + NumPatternsInString(str, pattern)
	endfor
	let b:Global_Word_Count = count_words
	return count_words
endf    

"returns the word count for the current line
"updates the buffer variable Current_Line_Number
"updates the buffer variable Current_Line_Word_Count
fu! CurrentLineWordCount()
	if b:Current_Line_Number != line(".") "if the line number has changed then add old count
		let b:Global_Word_Count = b:Global_Word_Count + b:Current_Line_Word_Count
	endif
	"calculate number of words on current line
	let line = getline(".")
	let pattern = "\\<\\(\\w\\|-\\|'\\)\\+\\>"
	let count_words = NumPatternsInString(line, pattern)
	let b:Current_Line_Word_Count = count_words "update buffer variable with current line count
	if b:Current_Line_Number != line(".") "if the line number has changed then subtract current line count
		let b:Global_Word_Count = b:Global_Word_Count - b:Current_Line_Word_Count
	endif
	let b:Current_Line_Number = line(".") "update buffer variable with current line number
	return count_words
endf    

"returns the word count for the entire file using variables defined in other procedures
"this is the function that is called repeatedly and controls the other word
"count functions.
fu! WordCount()
	if exists("b:Global_Word_Count") == 0
		let b:Global_Word_Count = 0
		let b:Current_Line_Word_Count = 0
		let b:Current_Line_Number = line(".")
		call OtherLineWordCount()
	endif
	call CurrentLineWordCount()
	return b:Global_Word_Count + b:Current_Line_Word_Count
endf

"returns the number of patterns found in a string
fu! NumPatternsInString(str, pat)
	let i = 0
	let num = -1
	while i != -1
		let num = num + 1
		let i = matchend(a:str, a:pat, i)
	endwhile
	return num
endf

"example of using the function for statusline:
"set statusline=wc:%{WordCount()}

"-------------------------------------------

set statusline=%<\%f\ %y%m%r\ wc:%{WordCount()}%=%l,%c%V\ \ %L\ lines:%P\  
set laststatus=2
