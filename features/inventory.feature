Feature: The store service back-end
    As a Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my items

Background:
    Given the following items
        | inv_name      | inv_sku | inv_quantity | inv_restock |
        | Rolex         | 123AB   | 5            | 2           |
        | Swatch        | 123VW   | 6            | 2           |
        | Harry Potter  | 123UY   | 6            | 10          |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Inventory RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create an Item
    When I visit the "Home Page"
    And I set the "name" to "Becoming"
    And I set the "sku" to "456MO"
    And I set the "quantity" to "5"
    And I set the "restock" to "2"
    And I press the "create" button
    Then I should see the message "Success"
    When I copy the "id" field
    And I press the "Clear" button
    Then the "id" field should be empty
    And the "Name" field should be empty
    And the "SKU" field should be empty
    And the "quantity" field should be empty
    And the "restock" field should be empty
    When I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see "Becoming" in the "Name" field
    And I should see "456MO" in the "SKU" field
    And I should see "5" in the "quantity" field
    And I should see "2" in the "restock" field

Scenario: List all inventory
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "Rolex" in the results
    And I should see "Swatch" in the results
    And I should not see "Becoming" in the results

Scenario: Search by SKU Item
    When I visit the "Home Page"
    And I set the "SKU" to "123AB"
    And I press the "Search" button
    Then I should see "Rolex" in the results
    And I should not see "Swatch" in the results
    And I should not see "Harry Potter" in the results

Scenario: Update an Inventory Item
    When I visit the "Home Page"
    And I set the "Name" to "Rolex"
    And I press the "Search" button
    Then I should see "Rolex" in the "Name" field
    And I should see "123AB" in the "SKU" field
    When I change "Name" to "Boxer"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Boxer" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "Boxer" in the results
    Then I should not see "Rolex" in the results

Scenario: Delete an Inventory Item
    When I visit the "Home Page"
    And I set the "Name" to "Rolex"
    And I press the "Search" button
    Then I should see "Rolex" in the "Name" field
    And I should see "123AB" in the "SKU" field
    And I should see "Rolex" in the results
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Item has been Deleted!"
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should not see "Rolex" in the results
    And I should see "Swatch" in the results
    And I should see "Harry Potter" in the results

Scenario: Query understocked
    When I visit the "Home Page"
    And I press the "restock" button
    Then I should see "Harry Potter" in the "Name" field