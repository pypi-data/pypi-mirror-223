libssp-py
===

A pure-Python implementation of the *Simple Streaming Protocol* (SSP), used by ImagineVision on their "Z CAM" cameras and accessories.

## Status

This Python implementation is mainly intended to ease further development and research into this protocol. While some care has been taken to make it perform well, lag is entirely expected. Once enough is known about the protocol, my plan is to re-write the library in Rust - that library will be intended for production use, while this one will remain for testing.

Is has only been tested with the [Z CAM IPMAN S](https://www.z-cam.com/ipman-s/), as I don't have any other Z CAM devices. If anyone can get this working with other devices, please let me know.

## Legal

This project is not affiliated with ImagineVision and does not use the official [libssp](https://github.com/imaginevision/libssp/). It was developed from scratch, primarily by analyzing the network traffic of the official SSP library and Z CAM mobile apps. 

It is licensed under the LGPL v3, meaning you are free to use it in both open-source and proprietary applications, however, any changes you make to the library itself must be published (preferably in a fork of this repository).