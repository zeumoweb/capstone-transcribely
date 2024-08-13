import Transcript from "./Transcript";
import Chat from "./Chat";
import Subtitle from "./Subtitle";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { Link } from 'react-router-dom';


function Edit() {
    const params = useParams();
    const type = params['type']
    const [src, setSrc] = useState('');
    const video_name = params['video_name']

    useEffect(() => {

        const fetchVideo = async () => {
            fetch(`http://127.0.0.1:5000/download/${video_name}`).then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.blob();
            })
                .then(blob => {
                    // Create a temporary URL for the blob
                    const url = window.URL.createObjectURL(blob);

                    setSrc(url);
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error);
                });
        };

        fetchVideo();
    }, []);
    return (
        <div className="flex h-screen">
            <div className="basis-[14.2%] pl-3 border-t border-r pt-4 h-screen">
                <Link to={`/edit/subtitle/${video_name}`}><div className="text-sm  w-[120px] p-2 hover:opacity-80 hover:text-[#36d7b7] hover:cursor-pointer"><i className="fa-regular fa-pen-to-square"></i> <span>Subtitle</span></div></Link>
                <Link to={`/edit/transcript/${video_name}`}><div className="text-sm p-2 hover:opacity-80 hover:text-[#36d7b7] hover:cursor-pointer"> <i className="fa-regular fa-file-lines"></i> <span>Transcript</span></div></Link>
                <Link to={`/edit/chat/${video_name}`}><div className="text-sm p-2 hover:opacity-80 hover:text-[#36d7b7] hover:cursor-pointer "><i className="fa-solid fa-comment"></i> <span>Chat</span></div></Link>

            </div>
            <div className="border-t w-full">
                <div className="flex flex-col items-center ">
                    <div className="text-center border-b-2 mb-4">
                        <video src={src} controls width="600px"></video>
                    </div>
                    {type === "transcript" && <Transcript />}
                    {type === "chat" && <Chat />}
                    {type === "subtitle" && <Subtitle />}

                </div>
            </div>
        </div>
    );
}

export default Edit;