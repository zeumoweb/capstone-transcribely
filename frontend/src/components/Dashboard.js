import Upload from "./Upload";
import { swappedLanguages } from './languages';
import { useEffect, useState } from "react";
import { Link }  from 'react-router-dom';

function Dashbaord() {
    const [videos, setVideos] = useState([]);

    useEffect(() => {
        const fetchVideos = async () => {
            const response = await fetch('http://127.0.0.1:5000/videos');
            if (!response.ok) {
                throw new Error(`Failed to fetch videos: ${response.status}`);
            }
            const data = await response.json();
            setVideos(data.videos);
        };
        fetchVideos();
    }, []);

    const download = async (event) => {
        const videoName = event.target.getAttribute('data-video');
        const response = await fetch(`http://127.0.0.1:5000/download/${videoName}`).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.blob();
        })
            .then(blob => {
                // Create a temporary URL for the blob
                const url = window.URL.createObjectURL(blob);

                // Create a link element to trigger the download
                const a = document.createElement('a');
                a.href = url;
                a.download = videoName + '.mp4'; // Set the desired filename
                document.body.appendChild(a);
                a.click();

                // Cleanup
                window.URL.revokeObjectURL(url);
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    };

    return (
        <div className="">
            <div className="w-full px-3 mt-8 border-solid border-2">
                <div className="flex justify-between my-4">
                    <div>
                        <div className="font-bold text-xl mb-2">Projects</div>
                        <div className="text-xs opacity-50">We make your videos more accessibe in seconds</div>
                    </div>

                    <Upload />
                </div>
                <div className="flex flex-col">
                    <div className="text-sm opacity-50 font-semibold my-2">
                        Today
                    </div>
                    {videos.map((video, index) => (
                        <div key={index} className="flex justify-between my-4">
                            <div className="flex basis-1/4">
                                <i className="fa-solid fa-video text-3xl"></i>
                                <div className="ml-2" >
                                    <div className="text-sm">{video.filename}.{video.format.split('/')[1]}</div>
                                    <div className="text-xs opacity-55">{video.duration}</div>
                                </div>
                            </div>
                            <div className="basis-1/10">
                                <span className="opacity-50 text-xs">Dimensions |</span> <span className="text-sm">{video.dimensions}</span>
                            </div>
                            <div className="basis-1/10">
                                <span className="opacity-50 text-xs">Size |</span> <span className="text-sm">{video.size}</span>
                            </div>
                            <div className="basis-1/10">
                                <span className="opacity-50 text-xs">Language |</span> <span className="text-sm">{swappedLanguages[video.target_language]}</span>
                            </div>
                            <div className="flex justify-between basis-1/4">
                                <Link className="border text-sm opacity-50 px-4 items-center py-1 hover:bg-black hover:text-white hover:cursor-pointer" to={`edit/subtitle/${video.filename}`}>View</Link>
                                <div className="border text-sm opacity-50 px-4 items-center py-1 hover:bg-black hover:text-white hover:cursor-pointer" data-video={video.filename} onClick={download} >Download</div>
                                <div className="border text-sm opacity-50 px-4 items-center py-1 hover:bg-black hover:text-white hover:cursor-pointer" data-video={video.filename}>Delete</div>
                            </div>

                        </div>

                    ))}

                </div>
            </div>
        </div>

    );
}

export default Dashbaord;