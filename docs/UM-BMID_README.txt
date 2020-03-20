
                        README - UM-BMID

                        Author: Tyson Reimer
                        Date: January 13, 2020

The folders within this Drive (https://bit.ly/UM-bmid) contain
the data that comprises the University of Manitoba Breast
Microwave Imaging Dataset.

The accompanying GitHub project can be found at:

    https://github.com/UManitoba-BMS/UM-BMID

-------------------------------------------------------------------------------
-------------------------------------------------------------------------------

                SECTION I: UM-BMID Folder Architecture
                --------------------------------------

The folder architecture is as follows:

/UM-BMID/
    The top directory

/UM-BMID/phantoms/

    ../gen-one/
        Contains the 3D-printable .stl files of the 3D-printed
        phantoms that comprise the first generation of phantoms

    ../gen-two/
        Contains the 3D-printable .stl files of the 3D-printed
        phantoms that comprise the second generation of phantoms

/UM-BMID/scan-data/

    ../docs/
        Contains documentation files for the dataset

    ../gen-one/ OR ../gen-two/

        ../clean/
            Contains clean .pickle and .mat files of the scan data,
            in the frequency domain after subtracting a reference scan.
            **NOTE: The files in this folder have had a reference scan
                    subtracted, either an empty-chamber reference,
                    indicated by the _emp suffix in the file name,
                    or an adipose-only phantom reference, indicated by
                    the _adi suffix in the file name.

        ../raw/
            Contains the raw .txt files from each experimental session
            as generated from the bed-system software during a scan.
            More info available in /UM-BMID/scan-data/docs/raw_files.txt.

        ../simple-clean/
            Contains ALL data from the scans (including reference
            scans), in the frequency-domain, and the corresponding
            metadata.
            **NOTE: No reference-scan subtraction has been performed
                    for the data contained here.

-------------------------------------------------------------------------------
-------------------------------------------------------------------------------

                        SECTION II: Finding a File
                        --------------------------

If you are looking for:

    Raw Data:
        Available in the ../raw/ folders

    Ready-to-use, no reference-subtraction data:
        Available in the ../simple-clean/ folders

    Ready-to-use, empty-chamber reference-subtraction:
        Available in the ../clean/ folders - these files have the _emp
        suffix

    Ready-to-use, adipose-only phantom reference subtraction:
        Available in the ../clean/ folders - these files have the _adi
        suffix

    Ready-to-use S11 data:
        Available in the ../clean/ and ../simple-clean/ folders - these
        files have s11 in their file names

    Ready-to-use S21 data:
        Available in the ../clean/ and ../simple-clean/ folders - these
        files have s21 in their file names

    Metadata:
        Available in the ../clean/ and ../simple-clean/ folders - these
        files contain all the above descriptors (s11, s21, _emp, _adi)
        and contain the prefix md or metadata in their file names

-------------------------------------------------------------------------------
-------------------------------------------------------------------------------

                        SECTION III: Suggested Use
                        --------------------------

The simplest way to start using UM-BMID is to download the files in:

    /UM-BMID/scan-data/{gen-two, gen-one}/simple-clean/

These files contain all S-parameter measurements from

The data files in this folder contain the frequency-domain S-parameters
before any reference-scan subtraction has been performed. The empty-chamber
reference scans for each sample can be found using the metadata file.

-------------------------------------------------------------------------------
-------------------------------------------------------------------------------

                        SECTION IV: Getting Help
                        ------------------------

The documentation files contained in /UM-BMID/scan-data/docs/ provide
more information regarding using the dataset, etc.

If you are interested in using UM-BMID, and unsure of where to begin,
please visit the project GitHub page at:

            https://github.com/UManitoba-BMS/UM-BMID

If you have any questions for the authors, you can contact them directly
at:

            UManitoba.BMS@gmail.com