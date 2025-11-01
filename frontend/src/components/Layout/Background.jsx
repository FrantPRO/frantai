const StaticBackground = () => (
    <div
        style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            backgroundImage: `image-set(
                url("/background.jpg") type("image/jpeg") 1x
            )`,
            backgroundSize: "cover",
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
            opacity: 0.12,
            zIndex: -1,
        }}
    />
);

export default StaticBackground;
