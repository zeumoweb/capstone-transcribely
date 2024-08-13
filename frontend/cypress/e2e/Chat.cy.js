describe('Chat Component', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/edit/chat/What_is_Networking'); // Replace '/chat' with the actual route for your chat component
  });

  it('should display existing messages', () => {
    const messages = [
      { role: 'user', content: 'Hello, how can I help you?' },
      { role: 'bot', content: 'Hi there!' },
    ];

    cy.get('#chat pre').should('have.length', messages.length);

    messages.forEach((message, index) => {
      cy.get(`#chat pre:nth-child(${index + 1})`)
        .should('have.text', message.content)
        .and('have.class', `bg-gray-300`);
    });
  });

  it('should allow typing and sending messages', () => {
    const newMessage = 'This is a new message.';

    cy.get('input[type="text"]').type(newMessage);
    cy.get('button').contains('Send').click();

    cy.get('#chat pre').last().should('have.text', newMessage);
    cy.get('#chat pre').last().should('have.class', 'bg-gray-300'); // Assuming user messages are blue
  });

  it('should clear the input field after sending a message', () => {
    cy.get('input[type="text"]').type('Another message');
    cy.get('button').contains('Send').click();

    cy.get('input[type="text"]').should('have.value', '');
  });
});
