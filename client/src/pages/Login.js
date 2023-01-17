import React, { useState } from 'react'
import "../styles/Login.css"
import { Button, Form, Input, Typography } from 'antd';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { useNavigate } from "react-router-dom";
import axios from 'axios';
import { useSignIn } from "react-auth-kit";

export default function Login() {
	const [email, setEmail] = useState("")
	const [password, setPassword] = useState("")
	const navigate = useNavigate()
	const signIn = useSignIn();


	// TODO: implement with API and stuff
	let submitLogIn = async (e) => {
		console.log("1")
		e.preventDefault()
		const resp = await axios.post("https://izifood.azurewebsites.net/api/loginUser?code=xKSI2S3EexvVi419ILcv4l6cQ6OrFmTKNO8M-iHqd8HrAzFuggm15g==", { email: email, password: password })
		console.log(resp.data)
		if (resp.data.result == true) {
			signIn({
				token: resp.data.token,
				expiresIn: 3600,
				tokenType: "Bearer",
				authState: { email: email,password: password },
			});
			document.cookie = "tabKey=dashboard";
			console.log("2")
			// localStorage.setItem("email", email)
			console.log(document.cookie)
			navigate("/dashboard")
		} else{
			alert("Wrong email / password")
		}
	}

	return (
		<div>
			<div className="centered-box">
				<Form>
					<Typography.Title level={3}>Login Page</Typography.Title>
					<Form.Item>
						<Input
							prefix={<UserOutlined />}
							placeholder="Email"
							onChange={(e) => { setEmail(e.target.value); }}
							value={email}
						/>
					</Form.Item>
					<Form.Item>
						<Input.Password
							prefix={<LockOutlined />}
							placeholder="Password"
							onChange={(e) => { setPassword(e.target.value); }}
							value={password}
						/>
					</Form.Item>

					<Form.Item>
						<Button onClick={submitLogIn} type="primary" htmlType="submit" block>
							Log in
						</Button>
						Or <a href="/signup">register now!</a>
					</Form.Item>

				</Form>

			</div>
		</div>
	)
}
