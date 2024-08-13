
import { Button, Navbar, NavbarBrand, NavbarCollapse, NavbarLink, NavbarToggle } from "flowbite-react";
import logo  from '../asset/images/logo2.png';
import { Link }  from 'react-router-dom';


export function NavBar(props) {
  return (
    <Navbar fluid className="bg-[#042B33]">
      <NavbarBrand href="/">
        <img src={logo} className="-ml-3 h-6 sm:h-9" alt="Flowbite React Logo" />
        <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white"></span>
      </NavbarBrand>
      <NavbarCollapse className="text-white ">
        <NavbarLink href="/" active>
          Home
        </NavbarLink >
        <NavbarLink href="/tools" className="text-white">Tools</NavbarLink>
        
        <div className="flex md:order-2">
          {!props.login && <NavbarLink href="/user/signp" className="text-white"><span className="hover:opacity-40 hover:text-black font-light text-sm rounded p-3 bg-[#3486a9]">Get started</span> </NavbarLink>}
          { props.login && <NavbarLink href="/user/login"><span className="mx-10 text-white hover:opacity-40">LOGIN</span> </NavbarLink> }
          {!props.login && <NavbarLink href="/user/login"><span className="mx-10 text-white hover:opacity-40">LOGOUT</span> </NavbarLink> }
        <NavbarToggle />
      </div>
      </NavbarCollapse>
    </Navbar>
  );
}
