texfile = cv.tex
pdffile = cv.pdf
outdir = pdf
auxfiles = cv.log cv.aux cv.out

compile :
	mkdir -p $(outdir) && pdflatex $(texfile) && mv $(pdffile) $(outdir)/$(pdffile) && make clean
	
clean :
	rm $(auxfiles)