#!/usr/bin/perl

use JSON qw( decode_json );
use Data::Dumper;
use JSON::Parse 'parse_json';

open(IN,'<:encoding(UTF-8)',"html_virustotal");

$json = JSON->new->allow_nonref;   
$decjson = $json->decode( <IN>);
my $sha=$decjson->{"sha256"};# !!!!!!!!!!!!!!!        A SUPPRIMER    !!!!!!!!!!!!!!!!!!!!!!
@tableau = ();
my $nomAV;
my $valeurDetection;
my $nomMalware;

foreach $key (keys %{$decjson->{scans}}){
    my $item = $decjson->{scans}{$key};
    if ($decjson->{scans}->{$key}->{detected}) {
    	unshift(@tableau,$key);
    }else {
    	push(@tableau,$key);
    }
};

open(OUT,'>:encoding(UTF-8)',"virustotal_$sha.log");
foreach my $v (@tableau) {
	$nomAv = $v;
	if ($decjson->{scans}->{$v}->{detected}) {
		$valeurDetection = "Dangereux";
		$nomMalware = $decjson->{scans}->{$v}->{result};
	} else {
		$valeurDetection = "Normal";
		$nomMalware = "";
	}
	write(OUT);
}
close(OUT);
close (IN);

format OUT =
@<<<<<<<<<<<<<<<<<<<<<<<< @<<<<<<<<< @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
$nomAv,$valeurDetection,$nomMalware;
.

format OUT_TOP =
@<<<<<<<<<<<<<<<<<<<<<<<< @<<<<<<<<< @<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
"Nom Antivirus","Statut","Complement"
---------------------     ---------- -----------------------

.