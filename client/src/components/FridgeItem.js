import React, { useState } from 'react';
import "../styles/Fridge.css"

function FridgeItem(props) {

  const [isEditing, setIsEditing] = useState(false);
  const [ingredient, setIngredient] = useState('Ingredient');
  const [amount, setAmount] = useState('Amount');
  const [unit, setUnit] = useState('Unit');

  function handleEditButtonClick() {
    setIsEditing(true);
  }

  function handleIngredientKeyDown(event) {
    if (event.key === 'Enter') {
      setIsEditing(false);
    }
  }

  function handleAmountKeyDown(event) {
    if (event.key === 'Enter') {
      setIsEditing(false);
    }
  }

  function handleUnitKeyDown(event) {
    if (event.key === 'Enter') {
      setIsEditing(false);
    }
  }

  return (
    <div className='ingredientBox'>
      <p className="ingredientName" contentEditable={isEditing} onKeyDown={handleIngredientKeyDown}>{props.ingredient}</p>
      <p className="unitName" contentEditable={isEditing} onKeyDown={handleAmountKeyDown}>{props.amount}</p>
      <p className="ingredientName" contentEditable={isEditing} onKeyDown={handleUnitKeyDown}>{props.unit}</p>
      <button className="pencil-button" onClick={handleEditButtonClick}></button>
    </div>
  );
}

export default FridgeItem;