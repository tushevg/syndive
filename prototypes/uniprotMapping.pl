#!/usr/bin/perl

use warnings;
use strict;

sub parseRecord($);

main:{
    my $file_uniprot = shift;
    my $record = "";
    open(my $fh, "gzcat $file_uniprot|") or die $!;
    print "protein\tgene\tproduct\tnote\tcount\n";
    while(<$fh>) {
        $record .= $_;
        if ($_ =~ m/^\/\//) {
            parseRecord($record);
            $record = "";
            #last;
        }
    }
    close($fh);
}

sub parseRecord($)
{
    my $record = $_[0];
    my $locus = ($record =~ m/LOCUS\s+(\w+)\s+/) ? $1 : "None";
    my $accession = ($record =~ m/\nACCESSION\s+([A-Z0-9]+)\s+/) ? $1 : "None";
    my $feature_gene = ($record =~ m/\n {5}(gene.*?)\n {5}[A-z]+/s) ? $1 : "None";
    my $gene = ($feature_gene =~ m/\/gene=\"(.*?)\"/s) ? $1 : "None";
    $gene = $locus if($gene eq "None");
    my $feature_protein = ($record =~ m/\n {5}(Protein.*?)\n {5}[A-z]+/s) ? $1 : "None";
    my $product = ($feature_protein =~ m/\/product=\"(.*?)\"\s+/s) ? $1 : "None";
    $product =~ s/\n//g;
    $product =~ s/\s+/ /g;
    my $note = ($feature_protein =~ m/\/note=\"(.*?)\"\s+/ms) ? $1 : "<note>";
    $note =~ s/\n//g;
    $note =~ s/\s+/ /g;
    my @notes = split("; ", $note);
    $product = shift(@notes) if($gene eq $product);
    
    my %test = ();
    foreach my $key (split("; ", $note)) {
        next if (exists($test{$key}));
        next if ($key eq $gene);
        next if ($key eq $product);
        $test{$key}++;
        #print $accession,"\t",$key,"\t","KnownName","\n";
    }
    print $accession,"\t",$gene,"\t",$product,"\t",join(";", sort keys(%test)),"\t",0,"\n";
}
