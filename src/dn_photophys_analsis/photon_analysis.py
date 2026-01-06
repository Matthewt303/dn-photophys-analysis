from file_io import load_image, save_localisation_table
from image_analysis import get_spots, get_spots_denoised
from single_mol_fitting import localise_frame
import time

def main():

    # SPECS #
    pix_res_um = 0.0975
    adu, gain, offset = 0.59, 1, 100

    frame_num, id = 1, 1

    localisations = []
    dn_localisations = []

    image_path = 'C:/users/mxq76232/Downloads/az_dn_photon_counts/d3_tubulin_af647_run3_3sep24.tif'
    denoised_im_path = 'C:/users/mxq76232/Downloads/az_dn_photon_counts/d3_dn_tubulin_af647_run3_3sep24.tif'
    out = 'C:/users/mxq76232/Downloads/az_dn_photon_counts'

    im_stack = load_image(image_path)
    dn_stack = load_image(denoised_im_path)

    start = time.time()

    for i in range(0, im_stack.shape[0]):

        frame = im_stack[i]
        dn_frame = dn_stack[i]

        image_spots, maxima_coords = get_spots(frame, pix_res_um)
        dn_image_spots, dn_maxima_coords = get_spots_denoised(dn_frame, frame, 
                                                              pix_res_um)

        frame_locs = localise_frame(image_spots,
                                    maxima_coords,
                                    pix_res=pix_res_um,
                                    frame_num=frame_num,
                                    id_num=id,
                                    adu=adu,
                                    gain=gain,
                                    offset=offset)
        
        dn_frame_locs = localise_frame(dn_image_spots,
                                    dn_maxima_coords,
                                    pix_res=pix_res_um,
                                    frame_num=frame_num,
                                    id_num=id,
                                    adu=adu,
                                    gain=gain,
                                    offset=offset)
        
        localisations.append(frame_locs)
        dn_localisations.append(dn_frame_locs)

        id += frame_locs.shape[0]
        frame_num += 1

        if frame_num % 100 == 0:

            print(
                "Processed " + str(frame_num) + "/" + str(im_stack.shape[0]) + " frames"
            )
    
    end = time.time()
    print(str(end - start) + ' seconds.')
    
    save_localisation_table(localisations, out)
    save_localisation_table(dn_localisations, out, denoised='y')

if __name__ == "__main__":

    main()
