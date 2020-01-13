## Metadata Information

This table provides descriptions for each piece of metadata recorded 
in each scan.

| Metadata String | Description |
| --------------- | ----------- |
| n_expt | The experiment number within that experimental session.
| | |
| id | The unique ID number of the experiment, with respect to the entire dataset. |
| | |
| phant_id | The ID tag of the phantom (ex: A3F4 indicates the scan was of the adipose shell A3 with fibroglandular shell F4).
| | |
| tum_rad | The radius of the tumor used in the scan, in centimeters. |
| | |
| tum_shape | The shape of the tumor in the scan. |
| | |
| tum_x | The x-position of the tumor, in centimeters, relative to the center of the imaging chamber.
| | |
| tum_y | The y-position of the tumor, in centimeters, relative to the center of the imaging chamber.
| | | 
| tum_z | The z-position of the tumor, in centimeters, relative to the top of the imaging chamber (where the chest wall would be).
| | |
| birads | The BI-RADS density class of the phantom. |
| | |
| adi_ref_id | The unique ID of the adipose-only reference scan for the experiment.
| | |
| emp_ref_id | The unique ID of the empty-chamber reference scan for the experiment.
| | |
| date | The date the scan was performed (format: YEAR-MONTH-DAY)|
| | |
| n_session | The number of the session in which the scan was performed. |
| | |
| ant_rad | The radial distance from the center of the imaging chamber of the SMA connection point on the antenna, measured in centimeters.
| | |
| ant_z | The height (z-position) of the antenna, with respect to the top of the imaging chamber (where the chest wall would be), in centimeters. |
| | |
| fib_ang | The polar angle of rotation of the fibroglandular shell, in degrees. The 0&deg; position for each shell is displayed in images in the `UM-BMID/scan-data/docs/` folder on the Google Drive. Positive angles indicate clockwise rotation of the shell.| 
| | |
| phant_x | The x-position of the center of the adipose shell, with respect to the center of the imaging chamber, in centimeters. |
| | |
| phant_y | The y-position of the center of the adipose shell, with respect to the center of the imaging chamber, in centimeters. |
| | | 
| fib_ref_id | The unique ID of a reference scan containing both adipose and fibroglandular tissue components. |
| | |
| fib_x | The x-position of the center of the fibroglandular shell, with respect to the center of the **adipose shell**, in centimeters.|
| | |
| fib_y | The y-position of the center of the fibroglandular shell, with respect to the center of the **adipose shell**, in centimeters.|
| | |
| tum_in_fib | Indicates if the tumor was located inside the fibroglandular shell. If equal to 1, then the tumor was in the shell. If equal to 0, then the tumor was in the adipose shell.
