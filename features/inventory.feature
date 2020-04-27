Feature: The store service back-end
    As a Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my items

Background:
    Given the following items
        | name          | inventory id | inventory sku | inventory quantity | inventory restock
        | Rolex         | 123456       | 123AB         | 5                  | 2
        | Swatch        | 234567       | 123VW         | 6                  | 2
        | Harry Potter  | 345678       | 123UY         | 6                  | 2

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Inventory Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create an Item
    When I visit the "Home Page"
    And I set the "Name" to "Becoming"
    And I set the "Inventory ID" to "5555555"
    And I set the "Inventory SKU" to "456MO"
    And I set the "Inventory quantity" to "5"
    And I set the "Inventory restock" to "2"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Inventory ID" field
    And I press the "Clear" button
    Then the "Inventory ID" field should be empty
    And the "Name" field should be empty
    And the "Inventory SKU" field should be empty
    And the "Inventory quantity" field should be empty
    And the "Inventory restock" field should be empty
    When I paste the "Inventory ID" field
    And I press the "Retrieve" button
    Then I should see "Becoming" in the "Name" field
    And I should see "5555555" in the "Inventory ID" field
    And I should see "456MO" in the "Inventory SKU" field
    And I should see "5" in the "Inventory quantity" field
    And I should see "2" in the "Inventory restock" field