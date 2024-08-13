// describe('Transcript Component', () => {
//     it('should display the text content', () => {
//       const text = 'This is some sample text.';
//       cy.mount(<Transcript content={text} />);
  
//       cy.get('#transcript').should('have.text', text);
//     });
  
//     it('should allow editing the text', () => {
//       const text = 'Initial text';
//       const newText = 'Edited text';
  
//       cy.mount(<Transcript content={text} />);
  
//       cy.get('#transcript').click().type(newText);
  
//       cy.get('#transcript').should('have.text', newText);
//     });
  
//     it('should download the content as a PDF', () => {
//       // Assuming downloadPDF is a function that triggers the PDF download
//       cy.stub(window, 'downloadPDF').as('downloadPDF');
  
//       const text = 'Text to download';
//       cy.mount(<Transcript content={text} />);
  
//       cy.get('button').contains('Download PDF').click();
  
//       cy.get('@downloadPDF').should('have.been.called');
//     });
//   });
  