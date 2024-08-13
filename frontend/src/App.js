import './App.css';
import { NavBar } from "./components/NavBar";
import Dashboard from "./components/Dashboard";
import Edit from './components/Edit';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

function App() {

  const BrowserRouter = createBrowserRouter([
    { path: '/', element: <Dashboard /> },
    { path: '/edit/:type/:video_name', element: <Edit /> },
  ]);
  return (
    <div className="App">
      <NavBar></NavBar>
      <RouterProvider router={BrowserRouter} />
    </div>
  );
}

export default App;
