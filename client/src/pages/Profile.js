import React, { useEffect, useState } from 'react'
import "../styles/Login.css"
import { Button, Form, Input, Typography, Select } from 'antd';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { getCookie, snake_to_natural, natural_to_snake } from "../utils/utils1"
export default function Profile() {

	const [user, setUser] = useState({})
	const [isLoading, setIsLoading] = useState(true)
	useEffect(() => {
		try {
			let user_tmp = JSON.parse(getCookie("_auth_state"))
			console.log('user_tmp', user_tmp)
			setUser(user_tmp)
			setIsLoading(false)
		} catch (e) {
			console.log(e)
		}
	}, [])

	console.log(user.email);
	return (isLoading) ? (<span>Loading. Please refresh the page if the loading takes too long.</span>) : (

		<div>
			<div className='profile-content-left'>
				<span style={{ "font-weight": "bold" }}>Menu</span>
				<ul className='leftMenu'>
					<li><a href='/favorite-recipes' className='a'>Favorite Recipes</a></li>
					<li><a href='/shopping-list' className='a'>Shopping list</a></li>
					<li><a href='/my-fridge' className='a'>Fridge Inventory</a></li>
					<li><a href='' className='a'>Money Spent</a></li>
				</ul>
			</div>
			<div className='profile-content-right'>
				<span style={{ "font-weight": "bold" }}>Profile</span>
				<Form>
					<img src={user.photo} style={{ width: "100px" }}></img>

					<Form.Item>
						<Input
							prefix={<UserOutlined />}
							placeholder="Name"
							value={user.name}
						/>
					</Form.Item>
					<Form.Item>
						<Input
							prefix={<UserOutlined />}
							placeholder="username"
							value={user.email}
						/>
					</Form.Item>

					<Form.Item>
						<Input.Password
							prefix={<LockOutlined />}
							placeholder="Password"
							value={user.password}
						/>
					</Form.Item>
					

				</Form>
			</div>
		</div>

	)
}
