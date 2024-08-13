import { useEffect, useState } from "react";
import { useParams } from 'react-router-dom';
import jsPDF from 'jspdf';

function Transcript() {
    const { video_name } = useParams();
    const [text, setText] = useState('');

    const downloadPDF = () => {
        const element = document.getElementsByClassName('content-to-download')[0];

        try {
            const doc = new jsPDF();
            doc.text(element.textContent, 10, 10); // Adjust text positioning as needed
            doc.save("transcript_" + video_name + ".pdf");
        } catch (error) {
            console.error('Error generating PDF:', error);
        }
    };

    useEffect(() => {
        const fetchText = async () => {
            const response = await fetch(`http://127.0.0.1:5000/download/transcript/${video_name}`);
            if (!response.ok) {
                throw new Error(`Failed to fetch videos: ${response.status}`);
            }
            const data = await response.json();
            setText(data.transcript);
        };

        fetchText();
    }, []);

    return (
        <div className="flex w-full flex-col items-center ">
            <pre id="transcript" contentEditable="true" className="content-to-download p-4 flex text-xs leading-6 flex-col bg-gray-100 w-[95%] rounded-md border border-[#ccc] overflow-y-scroll min-h-[200px] max-h-[300px] text-wrap focus:outline-none">
                {text}
            </pre>
            <button className="w-[95%] my-2 bg-slate-400 p-2 hover:opacity-50" onClick={downloadPDF}>Download PDF</button>
        </div>
    );
}

export default Transcript;