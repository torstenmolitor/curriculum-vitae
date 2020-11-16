\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{curriculum-vitae}[]

\LoadClass[a4paper]{article}

\RequirePackage{xcolor}
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{hyperref}
\RequirePackage{tabu}
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage{lipsum}
\RequirePackage{multicol}
\RequirePackage{fancyhdr}%

\newif\ifinenglish
\DeclareOption{english}{\inenglishtrue}
\DeclareOption{swedish}{}	% default option

\newif\ifuseportrait
\DeclareOption{portrait}{\useportraittrue}

\definecolor{subsectioncolor}{RGB}{0, 0, 0}
\definecolor{sectioncolor}{RGB}{0, 0, 0}	% default section title color is black

\DeclareOption{blue}{\definecolor{sectioncolor}{RGB}{40, 47, 128}}
\DeclareOption{turkoise}{\definecolor{sectioncolor}{RGB}{40, 122, 128}}
\DeclareOption{green}{\definecolor{sectioncolor}{RGB}{19, 133, 93}}
\DeclareOption{brown}{\definecolor{sectioncolor}{RGB}{128, 62, 40}}

\ProcessOptions\relax

\renewcommand*\familydefault{\sfdefault}

\ifinenglish
	\RequirePackage[english]{babel}
\else
	\RequirePackage[swedish]{babel}
\fi

\hypersetup{
    colorlinks=true,
    linkcolor=sectioncolor,
    urlcolor=sectioncolor,
}

\renewcommand{\section}{%
    \@startsection
    {section}{1}{0pt}	% {}{secnum-ish}{indentation}
	{1.1ex plus -1ex minus -1ex}	% above
    {.2ex plus .2ex}						% below
    {\large\bf\color{sectioncolor}}	% font spec.
}

\setcounter{secnumdepth}{0}	% no numbering of sections

\setlength\parindent{0pt}

\renewcommand{\labelitemi}{--}

\pagenumbering{gobble}