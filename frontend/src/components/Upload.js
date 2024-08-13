import React, { useState, CSSProperties } from 'react';
import ClipLoader from "react-spinners/ClipLoader";
import { languages } from './languages';

const Upload = () => {
  const [videoInfo, setVideoInfo] = useState({
    size: '',
    dimensions: '',
    duration: '',
    format: '',
    title: '',
    src: '',
    file: null
  });
  const [showModal, setShowModal] = useState(false);
  const [targetLang, settargetLang] = useState("en");
  const [originalLang, setoriginalLang] = useState("en");
  const [loading, setLoading] = useState(false);
  const [sub, setSub] = useState(false);
  const [dub, setDub] = useState(false);
  const [gender, setGender] = useState('');

  const override: CSSProperties = {
    display: "block",
    margin: "0 auto",
    borderColor: "#36d7b7",
  };

  const handleUploadClick = () => {
    document.getElementById('videoInput').click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const size = (file.size / (1000 * 1000)).toFixed(2) + ' MB'; // Convert size to MB
      const format = file.type;
      const title = file.name;

      const videoElement = document.createElement('video');
      videoElement.src = URL.createObjectURL(file);
      const src = videoElement.src

      videoElement.onloadedmetadata = () => {
        const dimensions = `${videoElement.videoWidth} x ${videoElement.videoHeight}`;
        const duration = `${Math.floor(videoElement.duration / 60)} min ${Math.floor(videoElement.duration % 60)} sec`;

        setVideoInfo({
          size,
          dimensions,
          duration,
          format,
          title,
          src,
          file
        });
      };
      setShowModal(true); // Show the modal
    }
  };


  const handleSubmit = async (event) => {
    event.preventDefault();
    setShowModal(false); // Hide the modal
    setLoading(true);
    const formData = new FormData();
    formData.append('title', videoInfo.title);
    formData.append('size', videoInfo.size);
    formData.append('dimensions', videoInfo.dimensions);
    formData.append('duration', videoInfo.duration);
    formData.append('original_language', originalLang);
    formData.append('target_language', targetLang);
    formData.append('file', videoInfo.file); // Append the video file
    formData.append('sub', sub);
    formData.append('dub', dub);
    formData.append('gender', gender);

    try {
      const response = await fetch('http://127.0.0.1:5000/subtitle/upload', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

    } catch (error) {
      console.error('Error:', error);
      alert(`Failed to upload data: ${error.message}`);
    }

    setLoading(false);
  };



  return (
    <div>
      <button
        onClick={handleUploadClick}
        className="bg-[#3486a9] hover:bg-[#0e313f] text-white font-bold py-2 px-4 rounded"
      >
        Upload Video
      </button>
      <input
        type="file"
        id="videoInput"
        className="hidden"
        accept="video/*"
        onChange={handleFileChange}
      />

      {loading && (
        <div className="z-10 fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
          <ClipLoader
            color="#36d7b7"
            loading={loading}
            cssOverride={override}
            size={200}
            aria-label="Loading Spinner"
            data-testid="loader"
          />
        </div>
      )}

      {showModal && (
        <div className="z-10 fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
          <div className="flex bg-white rounded-lg overflow-hidden shadow-xl max-w-screen-md w-full">
            <div className="flex-item basis-1/2 flex justify-center items-center  q">
              <video src={videoInfo.src} alt="Video Preview" className="mb-4 w-4/5 h-auto" ></video>
            </div>
            <div className="p-4 flex-item basis-1/2">
              <p className="text-md font-semibold mb-4">Video Information</p>
              <p className='my-2 text-xs'> <span className='font-semibold'>Title: </span>{videoInfo.title}</p>
              <p className='my-2 text-xs'> <span className='font-semibold'>Size of the video: </span>{videoInfo.size}</p>
              <p className='my-2 text-xs'> <span className='font-semibold'>Dimensions: </span>{videoInfo.dimensions}</p>
              <p className='my-2 text-xs'> <span className='font-semibold'>Duration: </span>{videoInfo.duration}</p>
              <p className='my-2 text-xs'> <span className='font-semibold'>Format: </span>{videoInfo.format}</p>
              <p className="text-md font-semibold mb-4">Configuration</p>
              <form onSubmit={handleSubmit} className="mt-4">
                <div className="mb-4">
                  <label htmlFor="videoLanguage" className="block text-xs font-bold mb-2">
                    Original Language
                    <p className='text-xs text-gray-500'>Language spoken in video</p>
                  </label>
                  <select id="languages" name="languages" onChange={(e) => setoriginalLang(e.target.value)} className="text-xs shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none">
                    <option key="auto" value="auto">Auto</option>
                    {Object.entries(languages).map(([language, code]) => (
                      <option key={code} value={code}>{language}</option>
                    ))}
                  </select>
                </div>
                <div className="mb-4">
                  <label htmlFor="videoLanguage" className="block text-xs font-bold mb-2">
                    Target Language
                    <p className='text-xs text-gray-500'>Language to be translated to</p>
                  </label>
                  <select id="languages" name="languages" onChange={(e) => settargetLang(e.target.value)} className="text-xs shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none">
                    {Object.entries(languages).map(([language, code]) => (
                      <option key={code} value={code}>{language}</option>
                    ))}
                  </select>
                </div>
                <div className="checkbox-container mb-2 flex justify-between flex-col text-sm w-1/3">
                  <div className='block text-xs font-bold mb-1'>Service</div>
                  <div className='flex justify-between'>
                    <label className="checkbox-label text-xs">
                      <input type="checkbox" checked={sub} className="checkbox-input" id="sub" name="option" onChange={(e) => setSub(!sub)} />
                      <span className="checkbox-custom ml-1"></span>
                      Sub
                    </label>
                    <label className="checkbox-label text-xs">
                      <input type="checkbox" checked={dub} className="checkbox-input" id="dub" onChange={() => setDub(!dub)} name="option" />
                      <span className="checkbox-custom ml-1"></span>
                      Dub
                    </label>
                  </div>
                </div>
                {dub && <div className="checkbox-container mb-2 flex justify-between flex-col text-sm w-1/3">
                  <div className='block text-xs font-bold mb-1'>Voice Type</div>
                  <div className='flex justify-between'>
                    <label className="checkbox-label text-xs">
                      <input type="radio" checked={gender == 'male'} value='male' id="male" name="option" onChange={(e) => setGender('male')} />
                      <span className="checkbox-custom ml-1"></span>
                      Male
                    </label>
                    <label className="checkbox-label text-xs">
                      <input type="radio" checked={gender == 'female'} value='female' id="female" onChange={(e) => { console.log(e.target.value); return setGender('female') }} name="option" />
                      <span className="checkbox-custom ml-1"></span>
                      Female
                    </label>
                  </div>
                </div>}

                <div className="flex items-center mt-4 justify-between">
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                  >
                    Cancel
                  </button>

                  <button
                    type="submit"
                    className="bg-[#3486a9] hover:bg-[#2e799a] text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                  >
                    Create
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Upload;
