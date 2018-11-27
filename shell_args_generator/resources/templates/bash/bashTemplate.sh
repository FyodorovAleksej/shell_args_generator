#!/bin/bash
%FLAGS%
while [ -n "$1" ]
do
	case "$1" in
%CASE%
	--) shift
	break;;
	*) echo "$1 is not an option"
	esac
shift
done

