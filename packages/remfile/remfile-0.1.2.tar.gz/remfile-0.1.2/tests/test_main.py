import h5py
import remfile

def test_example1():
    url = 'https://dandiarchive.s3.amazonaws.com/blobs/d86/055/d8605573-4639-4b99-a6d9-e0ac13f9a7df'

    file = h5py.File(remfile.File(url))

    assert file.attrs['neurodata_type'] == 'NWBFile'

    dataset = file['/processing/behavior/Whisker_label 1/SpatialSeries/data']
    assert dataset.shape == (217423, 2)