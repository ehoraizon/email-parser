import React, { useEffect, useState, useRef } from "react";
import * as ReactDOM from 'react-dom';
import Notificaiton from "./Notification";
import axios from 'axios';

const App = () => {
  const [emails, setEmails] = useState([]);
  const [notification, setNotification] = useState({});
  const notificationDelay = 2000;

  const castNotification = (success, title, message) => {
    setNotification({success, title, message})
    setTimeout(() => {
      setNotification({})
    }, notificationDelay)
  }

  useEffect(async () => {
    try {
      const response = await axios.get('/api/')

      let limit = response.data.limit
      let size = response.data.size
      let offset = response.data.offset + response.data.size

      setEmails(response.data.emails)
      
      while (size == limit) {
        const response = await axios.get(`/api/?offset=${offset}`)

        limit = response.data.limit
        size = response.data.size
        offset = response.data.offset + response.data.size
        setEmails(emails => [...emails, ...response.data.emails])
      }
    } catch (e) {
      castNotification(false, "Emails Transaction", "Error loading emails")
      console.log(e)
    }
  }, [])

  const msgFile = useRef(null)
  const compressedFile = useRef(null)

  const trashIcon = <svg className="w-4 cursor-pointer fill-red-500 hover:fill-red-900" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M135.2 17.69C140.6 6.848 151.7 0 163.8 0H284.2C296.3 0 307.4 6.848 312.8 17.69L320 32H416C433.7 32 448 46.33 448 64C448 81.67 433.7 96 416 96H32C14.33 96 0 81.67 0 64C0 46.33 14.33 32 32 32H128L135.2 17.69zM394.8 466.1C393.2 492.3 372.3 512 346.9 512H101.1C75.75 512 54.77 492.3 53.19 466.1L31.1 128H416L394.8 466.1z"/></svg>
  const fileImportIcon = <svg className="w-5 mr-2 cursor-pointer fill-green-600 hover:fill-green-700" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M384 0v128h128L384 0zM352 128L352 0H176C149.5 0 128 21.49 128 48V288h174.1l-39.03-39.03c-9.375-9.375-9.375-24.56 0-33.94s24.56-9.375 33.94 0l80 80c9.375 9.375 9.375 24.56 0 33.94l-80 80c-9.375 9.375-24.56 9.375-33.94 0C258.3 404.3 256 398.2 256 392s2.344-12.28 7.031-16.97L302.1 336H128v128C128 490.5 149.5 512 176 512h288c26.51 0 48-21.49 48-48V160h-127.1C366.3 160 352 145.7 352 128zM24 288C10.75 288 0 298.7 0 312c0 13.25 10.75 24 24 24H128V288H24z"/></svg>
  const compressedFilesIcon = <svg className="w-4 mr-2 cursor-pointer fill-green-600 hover:fill-green-700" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="M256 0v128h128L256 0zM224 128L224 0H48C21.49 0 0 21.49 0 48v416C0 490.5 21.49 512 48 512h288c26.51 0 48-21.49 48-48V160h-127.1C238.3 160 224 145.7 224 128zM96 32h64v32H96V32zM96 96h64v32H96V96zM96 160h64v32H96V160zM128.3 415.1c-40.56 0-70.76-36.45-62.83-75.45L96 224h64l30.94 116.9C198.7 379.7 168.5 415.1 128.3 415.1zM144 336h-32C103.2 336 96 343.2 96 352s7.164 16 16 16h32C152.8 368 160 360.8 160 352S152.8 336 144 336z"/></svg>

  const deleteEmail = async (email) => {
    try {
      await axios.delete(`/api/?id=${email.id}`)
      setEmails(emails => emails.filter(val => val.id != email.id))
      castNotification(true, "Email Transaction", `Email ${email.message_id} removed`)
    } catch (e) {
      castNotification(false, "Email Transaction", `Error removing email ${email.message_id}`)
      console.log(e)
    }
  }
  const submitEmailFile = async (e) => {
    if (e.target.files.length > 0) {
      try {
      const requestBody = new FormData();
      requestBody.append("msg", e.target.files[0], e.target.files[0].name);

      const response = await axios.post('/api/', requestBody, {
        headers: { 'Content-Type':  'multipart/form-data' }
      })
      
      setEmails(emails => [...emails, response.data])
      
      } catch (e) {
        if (e.response.status == 409) {
          castNotification(false, "Email Transaction", `Email already in db`)
        } else {
          castNotification(false, "Email Transaction", `Error uploading the email`)
        }
        console.log(e)
      }
    }
  }
  const submitCompressedFile = async (e) => {
    if (e.target.files.length > 0) {
      try {
      const requestBody = new FormData();
      requestBody.append("tar", e.target.files[0], e.target.files[0].name);

      const response = await axios.put('/api/', requestBody, {
        headers: { 'Content-Type':  'multipart/form-data' }
      })
      
      setEmails(emails => [...emails, ...response.data.emails])
      
      } catch (e) {
        castNotification(false, "Email Transaction", `Error uploading the emails`)
        console.log(e)
      }
    }
  }

  return (
    <div className="xl:content-auto p-5 max-w-7xl m-auto">
      { Object.keys(notification).length > 0 &&
        <div className="absolute z-50 inset-x-0 top-4">
          <Notificaiton 
            success={notification?.success} 
            title={notification?.title} 
            message={notification?.message} 
            delay={notificationDelay}
          />
        </div>
      }
      <input type="file" ref={msgFile} hidden onChange={submitEmailFile}/>
      <input type="file" ref={compressedFile} hidden onChange={submitCompressedFile}/>
      <div className="min-w-full block align-middle border-b border-gray-200 shadow sm:rounded-lg my-4">
        <div class="flex flex-col justify-center items-center sm:flex-row sm:justify-around p-2">
          <h3 class="py-2 text-center font-bold">Emails</h3>
          <button onClick={() => msgFile.current.click()}
            class="group my-2 sm:my-0 relative w-contain flex justify-center py-2 px-4 border-solid border-2 border-green-600 text-sm font-medium rounded-md text-gray-700 hover:text-black hover:border-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"  
          >
            {fileImportIcon}
            Upload Email
          </button>
          <button v-show="dateRangeSelected" onClick={() => compressedFile.current.click()}            
            class="group my-2 sm:my-0 relative w-contain flex justify-center py-2 px-4 border-solid border-2 border-green-600 text-sm font-medium rounded-md text-gray-700 hover:text-black hover:border-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"  
          >
            {compressedFilesIcon}
            Upload Compressed Emails
          </button>
        </div>
        <div class="min-w-full overflow-auto">
          <table class="min-w-full">
            <thead>
              <th
                class="px-6 py-3 text-xs font-medium leading-4 tracking-wider text-left text-gray-500 uppercase border-b border-gray-200 bg-gray-50"
              > </th>
              <th
                class="px-6 py-3 text-xs font-medium leading-4 tracking-wider text-left text-gray-500 uppercase border-b border-gray-200 bg-gray-50"
              >
                To
              </th>
              <th
                class="px-6 py-3 text-xs font-medium leading-4 tracking-wider text-left text-gray-500 uppercase border-b border-gray-200 bg-gray-50"
              >
                From
              </th>
              <th
                class="px-6 py-3 text-xs font-medium leading-4 tracking-wider text-left text-gray-500 uppercase border-b border-gray-200 bg-gray-50"
              >
                Date
              </th>
              <th
                class="px-6 py-3 text-xs font-medium leading-4 tracking-wider text-left text-gray-500 uppercase border-b border-gray-200 bg-gray-50"
              >
                Subject
              </th>
              <th
                class="px-6 py-3 text-xs font-medium leading-4 tracking-wider text-left text-gray-500 uppercase border-b border-gray-200 bg-gray-50"
              >
                Message-ID
              </th>
            </thead>
            <tbody>
            {
              emails.map((email, i) => 
                <tr>
                  <td onClick={() => deleteEmail(email)} 
                    class="px-6 py-3 border-b border-gray-200">
                      {trashIcon}
                  </td>
                  <td class="px-6 py-3 border-b border-gray-200 whitespace-nowrap"> { `${email.to_name} ${email.to_email}` } </td>
                  <td class="px-6 py-3 border-b border-gray-200 whitespace-nowrap"> { `${email.from_name} ${email.from_email}` } </td>
                  <td class="px-6 py-3 border-b border-gray-200 whitespace-nowrap"> { new Date(email.date).toLocaleString() } </td>
                  <td class="px-6 py-3 border-b border-gray-200 whitespace-nowrap"> { email.subject } </td>
                  <td class="px-6 py-3 border-b border-gray-200 whitespace-nowrap"> { email.message_id } </td>
                </tr>
              )
            }
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('app'));
root.render(<App/>);

export default App;