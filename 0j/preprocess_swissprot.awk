# Reduce SwissProt format text records to FASTA format (awking of earlier sed
# script
#
# The DE field is being truncated to a default length of 70. If a different length
# is preferred use the command line set variable -v DELEN=N for length N, or -1 for
# no truncation 
#
# The OS field is not added to headers unless commandline variable -v ADDOS=1 set
# The OC field is not added to headers unless commandline variable -v ADDOC=1 as
# well as OS

function reset_fields() {
  ID=""; AC="";
  DE=""; OS=""; OC=""
}

BEGIN {
   reset_fields()
   if(DELEN == 0)
      DELEN = 70
}

/^  / {
  gsub(" ", "", $0)
  print $0
  next
}

/^[CFRKG]/ {next}

/^D/ {		# Also removes DR
  if($0 ~ /^DE /)
    {
    x = $0
    sub("DE  *", "", x)
    if(DE == "")
      DE = x
    else if (DE ~ /-$/)
      DE = sprintf("%s%s", DE, x)
    else
      DE = sprintf("%s %s", DE, x)
    }
  next
}

/^O/ {		# Also removes OC
  if(ADDOS && $0 ~ /^OS / && OS == "")
    {
    OS = $0
    sub("OS  *", "", OS)
    sub("[;.]", "", OS)  # Delete suffix ; or .
    }

  if(ADDOC && $0 ~ /^OC / && OC == "")
    {
    x = $0
    sub("OC  *", "", x)
    if(OC == "")
      OC = x
    else if (OC ~ /-$/)
      OC = sprintf("%s%s", OC, x)
    else
      OC = sprintf("%s %s", OC, x)
    sub("[.]$", "", OS)
    }

  next
}

/^ID / {
  if(ID == "")
    ID = $2
  next
}

/^AC / {
  if(AC == "")
    {
    AC = $2
    sub("[;.]", "", AC)  # Delete suffix ; or .
    }
  next
}

/^SQ / {
  if (DE != "")
    {
    sub("[.]$", "", DE)
    if (DELEN > 0)
      DE = substr(DE, 1, DELEN)
    }
  else
    DE="."
  if(ADDOS)
    printf(">%s\t%s\t%s %s\n",ID, AC, DE, OS)
  else
    printf(">%s\t%s\t%s\n", ID, AC, DE)
  reset_fields()
  next
}
