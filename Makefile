AUX_DIR:=./aux
NAME:=bakalaurinis
TEX_NAME:=$(NAME).tex
PDF_NAME:=$(NAME).pdf
LATEXMK_BASE_FLAGS:=-lualatex -file-line-error -interaction=nonstopmode -emulate-aux-dir -aux-directory=$(AUX_DIR) -halt-on-error

.PHONY: pdf
pdf: reset-part dirs
	latexmk $(LATEXMK_BASE_FLAGS) $(TEX_NAME)

.PHONY: strict
strict: reset-part dirs
	latexmk $(LATEXMK_BASE_FLAGS) -Werror $(TEX_NAME)

.PHONY: watch
watch: reset-part dirs
	latexmk $(LATEXMK_BASE_FLAGS) -pvc -view=none $(TEX_NAME)

includeonly.tex:
	@[ "${PART}" ] || ( echo ">> PART is not set"; exit 1 )
	@printf '\\begin{document}\n\\include{%s}\n\\end{document}\n' "$(PART)" > includeonly.tex
	@echo "Watching only: $(PART)"

.PHONY:
reset-part:
	@rm -f includeonly.tex

.PHONY: part
part: includeonly.tex dirs
	latexmk $(LATEXMK_BASE_FLAGS) $(TEX_NAME)

.PHONY: watch-part
watch-part: includeonly.tex dirs
	latexmk $(LATEXMK_BASE_FLAGS) -pvc -view=none $(TEX_NAME)

.PHONY: dirs
dirs:
	find chapters -type d -exec mkdir -p out/{} \;
	find chapters -type d -exec mkdir -p aux/{} \;

# .PHONY: wordcount
# wordcount:
# 	texcount -total -utf8 $(TEX_NAME)
#
# .PHONY: check
# check:
# 	chktex $(TEX_NAME)

.PHONY: clean
clean:
	rm -rf out/
	rm -f ${PDF_NAME}
