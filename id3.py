import mutagen
from mutagen.easyid3 import EasyID3



def set_id3_tag(file_path, title=None, artist=None, albumartist=None, album=None, genre=None,
                track_num=None, total_track_num=None, disc_num=None, total_disc_num=None):
    try:
        tags = EasyID3(file_path)
    except mutagen.id3.ID3NoHeaderError:
        tags = mutagen.File(file_path, easy=True)
        tags.add_tags()

    if title:
        tags['title'] = title
    if artist:
        tags['artist'] = artist
    if albumartist:
        tags['albumartist'] = albumartist
    if album:
        tags['album'] = album
    if genre:
        tags['genre'] = genre
    if total_track_num:
        if track_num:
            tags['tracknumber'] = '{}/{}'.format(track_num, total_track_num)
        else:
            tags['tracknumber'] = '/{}'.format(total_track_num)
    else:
        if track_num:
            tags['tracknumber'] = '{}'.format(track_num)
    if total_disc_num:
        if disc_num:
            tags['discnumber'] = '{}/{}'.format(disc_num, total_disc_num)
        else:
            tags['discnumber'] = '/{}'.format(total_disc_num)
    else:
        # if track_num:
        if disc_num:
            tags['discnumber'] = '{}'.format(disc_num)

    tags.save()

def show_id3_tags(file_path):
    tags = EasyID3(file_path)
    print(tags.pprint())

def delete_id3_tag(file_path, target_tag):
    tags = EasyID3(file_path)
    tags.pop(target_tag, None)
    tags.save()

def delete_all_id3_tag(file_path):
    tags = EasyID3(file_path)
    tags.delete()
    tags.save()