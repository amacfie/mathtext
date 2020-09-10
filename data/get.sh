#!/bin/bash
rm -rf documents
mkdir documents
echo "{}" > index.json

if [[ -z "$MATHTEXT_NUM_TARS" ]]; then
  MATHTEXT_NUM_TARS=2
fi
if ((MATHTEXT_NUM_TARS > 0)); then
  # https://arxiv.org/help/bulk_data_s3#src
  s3cmd get s3://arxiv/src/arXiv_src_manifest.xml --requester-pays --force
  python3 ./s3cmds.py $MATHTEXT_NUM_TARS > ./s3cmds.txt

  # https://stackoverflow.com/a/1521498
  while IFS="" read -r p || [ -n "$p" ]
  do
    eval $p
    mkdir gzfiles

    for f in ./*.tar; do
      tar --strip-components=1 -xvf $f -C ./gzfiles
      rm $f
    done

    cd ./gzfiles

    # some .gz files are compressed files
    # https://unix.stackexchange.com/a/474807
    for f in ./*.gz; do
      # https://stackoverflow.com/a/31195882
      if file $f | grep -q 'tex'; then
        gunzip $f
        mv `basename $f .gz` `basename $f .gz`.tex
      fi
    done

    # some .gz files are compressed folders
    for f in ./*.gz; do
      # https://unix.stackexchange.com/a/535624
      sem -j +0 "tar --wildcards -zxvf $f '*.tex' --one-top-level"
    done
    sem --wait

    cd ../

    python3 ./proc_arxiv.py

    rm -rf ./gzfiles
  done < ./s3cmds.txt
  rm ./s3cmds.txt ./arXiv_src_manifest.xml
fi

if [[ -z "$MATHTEXT_SKIP_SE" ]]; then
  wget https://archive.org/download/stackexchange/math.stackexchange.com.7z
  7z x math.stackexchange.com.7z -omath.stackexchange.com
  python3 proc_qs.py math.stackexchange.com/Posts.xml math.stackexchange.com
  wget https://archive.org/download/stackexchange/cstheory.stackexchange.com.7z
  7z x cstheory.stackexchange.com.7z -ocstheory.stackexchange.com
  python3 proc_qs.py cstheory.stackexchange.com/Posts.xml cstheory.stackexchange.com
  wget https://archive.org/download/stackexchange/mathoverflow.net.7z
  7z x mathoverflow.net.7z -omathoverflow.net
  python3 proc_qs.py mathoverflow.net/Posts.xml mathoverflow.net

  rm -rf ./mathoverflow* ./cstheory* ./math.*
fi

if [[ -z "$MATHTEXT_SKIP_PROJECTS" ]]; then
  mkdir texstuff
  cd texstuff
  git clone --depth=1 https://github.com/OpenLogicProject/OpenLogic.git
  python3 ../proc_tex_proj.py OpenLogic https://github.com/OpenLogicProject/OpenLogic
  git clone --depth=1 https://github.com/Ben-McKay/concrete-algebra.git
  python3 ../proc_tex_proj.py concrete-algebra https://github.com/Ben-McKay/concrete-algebra
  git clone --depth=1 https://github.com/ULeth-Math-CS/APEXCalculusV4.git
  python3 ../proc_tex_proj.py APEXCalculusV4 https://github.com/ULeth-Math-CS/APEXCalculusV4
  git clone --depth=1 https://github.com/ULeth-Math-CS/Math1410-Text.git
  python3 ../proc_tex_proj.py Math1410-Text https://github.com/ULeth-Math-CS/Math1410-Text
  git clone --depth=1 https://github.com/ULeth-Math-CS/Math1010Text.git
  python3 ../proc_tex_proj.py Math1010Text https://github.com/ULeth-Math-CS/Math1010Text
  git clone --depth=1 https://github.com/ULeth-Math-CS/CalculusTexts.git
  python3 ../proc_tex_proj.py CalculusTexts https://github.com/ULeth-Math-CS/CalculusTexts
  git clone --depth=1 https://github.com/jirilebl/ra.git
  python3 ../proc_tex_proj.py ra https://github.com/jirilebl/ra
  git clone --depth=1 https://github.com/HoTT/book.git
  python3 ../proc_tex_proj.py book https://github.com/HoTT/book
  git clone --depth=1 https://gitlab.com/jim.hefferon/linear-algebra.git
  python3 ../proc_tex_proj.py linear-algebra https://gitlab.com/jim.hefferon/linear-algebra
  git clone --depth=1 https://github.com/jirilebl/diffyqs.git
  python3 ../proc_tex_proj.py diffyqs https://github.com/jirilebl/diffyqs.git
  git clone --depth=1 https://github.com/boazbk/crypto.git
  python3 ../proc_tex_proj.py crypto https://github.com/boazbk/crypto.git
  git clone --depth=1 https://github.com/boazbk/tcs.git
  python3 ../proc_tex_proj.py tcs https://github.com/boazbk/tcs.git

  mkdir book
  wget https://www.gutenberg.org/files/38769/38769-t/38769-t.tex -O book/tex.tex
  python3 ../proc_tex_proj.py book https://www.gutenberg.org/ebooks/38769
  mkdir book
  wget https://www.gutenberg.org/files/31076/31076-t/31076-t.tex -O book/tex.tex
  python3 ../proc_tex_proj.py book https://www.gutenberg.org/ebooks/31076
  mkdir book
  wget https://www.gutenberg.org/files/36959/36959-t/36959-t.tex -O book/tex.tex
  python3 ../proc_tex_proj.py book https://www.gutenberg.org/ebooks/36959
  mkdir book
  wget https://www.gutenberg.org/files/33283/33283-t/33283-t.tex -O book/tex.tex
  python3 ../proc_tex_proj.py book https://www.gutenberg.org/ebooks/33283
  mkdir book
  wget https://www.gutenberg.org/files/13693/13693-t/13693-t.tex -O book/tex.tex
  python3 ../proc_tex_proj.py book https://www.gutenberg.org/ebooks/13693
  mkdir book
  wget https://www.gutenberg.org/files/36670/36670-t/36670-t.tex -O book/tex.tex
  python3 ../proc_tex_proj.py book https://www.gutenberg.org/ebooks/36670
  mkdir book
  wget https://www.gutenberg.org/files/40395/40395-t/40395-t.tex -O book/tex.tex
  python3 ../proc_tex_proj.py book https://www.gutenberg.org/ebooks/40395

  wget https://www1.essex.ac.uk/maths/people/fremlin/mt1.2011/mt1.2011.tar.gz
  unp mt1.2011.tar.gz -o files
  python3 ../proc_tex_proj.py files https://www1.essex.ac.uk/maths/people/fremlin/mt1.2011/mt1.2011.tar.gz
  wget https://www1.essex.ac.uk/maths/people/fremlin/mt2.2016/mt2.2016.tar.gz
  unp mt2.2016.tar.gz -o files
  python3 ../proc_tex_proj.py files https://www1.essex.ac.uk/maths/people/fremlin/mt2.2016/mt2.2016.tar.gz
  wget https://www1.essex.ac.uk/maths/people/fremlin/mt3.2012/mt3.2012.tar.gz
  unp mt3.2012.tar.gz -o files
  python3 ../proc_tex_proj.py files https://www1.essex.ac.uk/maths/people/fremlin/mt3.2012/mt3.2012.tar.gz
  wget https://www1.essex.ac.uk/maths/people/fremlin/mt4.2013/mt4.2013.tar.gz
  unp mt4.2013.tar.gz -o files
  python3 ../proc_tex_proj.py files https://www1.essex.ac.uk/maths/people/fremlin/mt4.2013/mt4.2013.tar.gz
  wget https://www1.essex.ac.uk/maths/people/fremlin/mt5.2015/mt5.2015.tar.gz
  unp mt5.2015.tar.gz -o files
  python3 ../proc_tex_proj.py files https://www1.essex.ac.uk/maths/people/fremlin/mt5.2015/mt5.2015.tar.gz

  cd ../
  rm -rf ./texstuff
fi

python3 ./post_proc.py

du -sh ./documents

