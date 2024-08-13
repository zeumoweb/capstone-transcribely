// import React from 'react';
// const data = [
//   { id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },
//   { id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },
//   { id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },
//   { id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },
//   { id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },
//   { id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },
//   { id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },
//   { id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },
//   { id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },
//   { id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },
//   { id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },
//   { id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },
//   { id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },
//   { id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },{ id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },
//   { id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },{ id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },{ id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },{ id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },{ id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },{ id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },{ id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },{ id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },{ id: 1, name: 'Alice', age: 30 },
//   { id: 2, name: 'Bob', age: 25 },
//   // ... more data objects
// ];

// const headers = ['id', 'name', 'age'];


// const TableWithScroll = () => {
//   return (
//       <table style={{ height: '100px', overflowY: 'auto' }}>
//         <thead style={{ position: 'sticky', top:0}}>
//           <tr >
//             {headers.map((header) => (
//               <th key={header}>{header}</th>
//             ))}
//           </tr>
//         </thead>
//         <tbody>
//           {data.map((row) => (
//             <tr key={row.id || Math.random()}>
//               {headers.map((header) => (
//                 <td key={header}>{row[header]}</td>
//               ))}
//             </tr>
//           ))}
//         </tbody>
//       </table>
//   );
// };

// export default TableWithScroll;


