import argparse
import ffmpeg
import os


##############################
# Process track listing text #
##############################

def get_track_listings(path):
    ''' Read the track listing from a file.
    Return a list of tuples representing the track titles and starting timestamps.

    Example:
    [..., ("Lucky I Got What I Want", "37:05"), ("Drops", "42:09"), ...]
    '''
    with open(path) as file_:
        listings = file_.read().splitlines()

    return [split_track_listing_to_components(listing) for listing in listings]


def split_track_listing_to_components(listing):
    ''' A listing is a line of raw text. Example:
        TITLE START_TIMESTAMP
        Lucky I Got What I Want 37:05

        This function splits the line into its components, the title and the timestamp.
        Example: ("Lucky I Got What I Want", "37:05")
    '''
    raw_components = listing.split(' ')

    title = ' '.join(raw_components[:-1])
    start_timestamp = raw_components[-1]

    return {'title': title, 'start_time': start_timestamp}


##################################
# Execute the split using ffmpeg #
##################################

def generate_track(input_path, output_path, title, track_number, start_time, end_time=None):
    ''' Trim an audio track and tag it with metadata.
    Example arguments:
    input_path: "/home/jungle-la-cigale.mp3"
    output_path: "/home/jungle-la-cigale/Platoon.mp3"
    title: "Platoon"
    track_number: 2
    start_time: "6:46"
    end_time: "11:11"
    '''

    # Set the start and end timestamps for the track using the ffmpeg formatting keys
    # "end_time" will be absent for the last track, so only set it when present
    time_bounds = {'ss': start_time}
    if end_time:
        time_bounds['to'] = end_time

    # The order isn't important, but ffmpeg requires each metadata item to be added as its own key
    metadata = {
        'metadata:g:0': f'title={title}',
        'metadata:g:1': f'track={track_number}'
    }

    (ffmpeg.
        input(
            input_path,
            **time_bounds
        )
        .output(
            output_path,
            acodec='copy',
            **metadata)
        .overwrite_output()
        .run()
    )


##############
# Entrypoint #
##############

def get_args():
    argparser = argparse.ArgumentParser()

    argparser.add_argument('--input', help='Path to the input audio file')
    argparser.add_argument('--output_dir', help='Path to a directory where output audio files will be put')
    argparser.add_argument('--listings', help='Path to a text file containing a track listing')

    args = argparser.parse_args()

    return args


def add_track_numbers(listings):
    ''' Add the track number to each listing. '''
    return [
        {**listing, 'track_number': index}
        for index, listing in enumerate(listings, start=1)
    ]


def add_end_times(listings):
    ''' Peek ahead to the next track and get its start time, set that as the end_time for the preceding track. '''
    listings_with_end_times = [
        {**listing, 'end_time': next_listing['start_time']}
        for (listing, next_listing) in zip(listings, listings[1:])
    ]
    
    # The final track was dropped in the last stage, add it back here with no end_time
    return listings_with_end_times + listings[-1:]


def make_filename(track_listing):
    ''' Given a track, return a filename that is composed of the track title and the ".mp3" file extension. '''
    return track_listing['title'] + '.mp3'


def main(input_path, output_directory, listings_path):
    ''' Read the track listings from a file and generate the tracks.
    For each track, a copy of the input audio file is trimmed to the proper start and
    end times, track metadata is added and the file is written to the output directory.
    '''
    listings = get_track_listings(listings_path)
    listings = add_track_numbers(listings)
    listings = add_end_times(listings)

    for listing in listings:
        output_filename = make_filename(listing)
        output_path = os.path.join(output_directory, output_filename)
        generate_track(input_path, output_path, **listing)


if __name__ == '__main__':
    ARGS = get_args()
    main(ARGS.input, ARGS.output_dir, ARGS.listings)
