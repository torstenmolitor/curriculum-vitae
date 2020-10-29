\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cv}[]
\RequirePackage{xcolor}
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}

\newif\ifinenglish
\DeclareOption{english}{\inenglishtrue}
\DeclareOption{swedish}{}	% default option

\newif\ifuseportrait
\DeclareOption{portrait}{\useportraittrue}

\definecolor{subsectioncolor}{RGB}{0, 0, 0}
\definecolor{sectioncolor}{RGB}{36, 56, 156}

\renewcommand*\familydefault{\sfdefault}

\ProcessOptions\relax
\LoadClass[a4paper]{article}

\RequirePackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=sectioncolor,
    urlcolor=sectioncolor,
}

\RequirePackage{tabu}
\RequirePackage{graphicx}
\RequirePackage{geometry}

\renewcommand{\section}{%
    \@startsection
    {section}{1}{0pt}
	{0ex plus -1ex minus -1ex}%
    {1ex plus .2ex}{\Large\color{sectioncolor}}%
}

\setcounter{secnumdepth}{0}	% no numbering of sections

\ifinenglish
	\RequirePackage[english]{babel}
\else
	\RequirePackage[swedish]{babel}
\fi

\newcommand{\icon}[1]{\alignbox{\includegraphics[width=1em]{icons/#1}}{c}}

\newcommand{\entry}[6]{{\bf \textcolor{subsectioncolor}{#1}}, \textcolor{subsectioncolor}{#2} \hfill {\small \it #3 -- #4} \newline
\begin{tabu} to \linewidth {X[\leftcol, l] | X[\rightcol, l]}
{\small \it #5} & {\small #6}
\end{tabu}
\vspace*{2pt}}

\newcommand{\alignbox}[2]{\begingroup
\setbox0=\hbox{#1}%
\parbox[#2]{\wd0}{\box0}
\endgroup}

\setlength\parindent{0pt}

\renewcommand{\labelitemi}{--}

\pagenumbering{gobble}