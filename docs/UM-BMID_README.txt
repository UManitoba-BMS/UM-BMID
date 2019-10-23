
                        README - UM-BMID

                        Author: Tyson Reimer
                        Date: October 21st, 2019

The folders within this Drive contain the data that comprises the
University of Manitoba Breast Microwave Imaging Dataset.

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
            in the frequency domain, in the time-domain after conversion
            via the inverse discrete Fourier transform, and in the time
            domain after conversion via the inverse chirp z-transform.
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
            Contains ALL data from the scans, in the frequency-domain,
            and the corresponding metadata.
            **NOTE: No reference-scan subtraction has been performed
                    for the data contained here.

-------------------------------------------------------------------------------
-------------------------------------------------------------------------------

                        SECTION II: Suggested Use
                        -------------------------

The simplest way to start using UM-BMID is to download the files in:

    /UM-BMID/scan-data/{gen-two, gen-one}/simple-clean/

The data in gen-one is limited to 249 phantom scans, while gen-two will
contain data from 1008 phantom scans at completion. We recommend using gen-two
for this reason, and because of the more extensive metadata recorded for scans
in gen-two.

The data files in this folder contain the frequency-domain S-parameters
before any reference-scan subtraction has been performed. The empty-chamber
reference scans for each sample can be found using the metadata file.

-------------------------------------------------------------------------------
-------------------------------------------------------------------------------

                        SECTION III: Getting Help
                        -------------------------

The documentation files contained in /UM-BMID/scan-data/docs/ provide
more information regarding using the dataset, etc.

If you are interested in using UM-BMID, and unsure of where to begin,
please visit the project GitHub page at:

            https://github.com/UManitoba-BMS/UM-BMID

If you have any questions for the authors, you can contact them directly
at:

            UManitoba.BMS@gmail.com