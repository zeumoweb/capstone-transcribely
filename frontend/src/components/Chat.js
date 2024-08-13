import { useState } from "react";
import { useParams } from 'react-router-dom';

function Chat() {
    const [messages, setMessages] = useState([{ ai: "ai", content: "Hello, how can I help you?" }, { ai: "ai", content: "Ask me anything concerning the above video" }]);
    const [input, setInput] = useState('');
    const { video_name } = useParams();

    const handleSend = async () => {
        if (input.trim() === '') return;

        const userMessage = { role: 'user', content: input };
        setMessages([...messages, userMessage]);
        setInput('');

        // Call your backend API here
        const response = await fetch(`http://127.0.0.1:5000/ask/${video_name}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: input }),
        });
        if (!response.ok) {
            const aiMessage = { role: 'ai', content: "Please Retry" };
            setMessages([...messages, userMessage, aiMessage]);
            return;
        }
        const reader = response.body.getReader();
        const chat = document.getElementById('chat');
        const answer = document.createElement('pre');
        answer.className = 'p-4 rounded-lg w-max-1/2 text-wrap bg-gray-300 text-black self-start';
        chat.appendChild(answer);

        let output = '';
        const container = document.getElementById('container');
        while (true) {
            const { done, value } = await reader.read();
            const chunk = new TextDecoder('utf-8').decode(value);
            output += chunk;
            answer.innerHTML = output;
            container.scrollTop = container.scrollHeight;
            if (done) {
                break;
            }
        }
        chat.removeChild(answer);
        const aiMessage = { role: 'ai', content: output };
        setMessages([...messages, userMessage, aiMessage]);
    };




    return (
        <div className="flex flex-col basis-[1/2] w-full pb-6 items-center border overflow-y-auto">
            <div className="flex text-xs leading-8 flex-col h-screen bg-gray-100 w-[95%] rounded-md border border-[#ccc] overflow-y-scroll min-h-[200px] max-h-[300px] focus:outline-none text-wrap">
                <div id="container" className="flex-grow p-6 overflow-auto">
                    <div id="chat" className="flex flex-col space-y-4">
                        {messages.map((message, index) => (
                            <pre
                                key={index}
                                className={`p-2 px-4 rounded-lg w-max-1/2 text-wrap  ${message.role === 'user' ? 'bg-blue-500 text-white self-end' : 'bg-gray-300 text-black self-start'
                                    }`}
                            >
                                {message.content}
                            </pre>
                        ))}
                    </div>
                </div>

            </div>
            <div className="bg-white w-[1000px] mt-2 flex">
                <input
                    type="text"
                    className="flex-grow border rounded p-2"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => {
                        if (e.key === 'Enter') handleSend();
                    }}
                />
                <button
                    className="bg-blue-500 text-white p-2 ml-2 rounded"
                    onClick={handleSend}
                >
                    Send
                </button>
            </div>
        </div>
    );
}

export default Chat;